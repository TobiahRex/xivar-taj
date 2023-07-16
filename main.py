import os
import requests
import PyPDF2
import json
import re
from PIL import Image
from dotenv import load_dotenv
import logging
import backoff
from datetime import datetime as dt
import openai
import time
from elevenlabs import set_api_key, generate, voices, play
from openai.error import (
    APIError,
    OpenAIError,
    ServiceUnavailableError,
    APIConnectionError,
    Timeout,
    TryAgain,
    RateLimitError,
)
import tiktoken

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_and_replace_doc_folder(new_root, old_root):
    if new_root != old_root:
        if os.path.exists(old_root):
            if not os.path.exists(new_root):
                os.mkdir(new_root)
            # Traverse the contents of the original directory
            for item in os.listdir(old_root):
                item_path = os.path.join(old_root, item)

                # Move files and subdirectories to the new directory
                new_item_path = os.path.join(new_root, item)
                os.rename(item_path, new_item_path)

            # Remove the original (now empty) directory
            os.rmdir(old_root)


def get_data_by_url(url):
    original_filename = url.split("/")[-1]
    arxiv_number = original_filename.split(".pdf")[0]
    arxiv_dir = os.path.join("downloads", arxiv_number)
    metadata_filename = os.path.join(arxiv_dir, "metadata.txt")
    metadata = {}
    with open(metadata_filename, "r") as f:
        metadata = json.load(f)
    return arxiv_dir, arxiv_number, metadata

def get_metadata_by_folder(folder):
    metadata_filename = os.path.join(folder, "metadata.txt")
    metadata = {}
    with open(metadata_filename, "r") as f:
        metadata = json.load(f)
    return metadata


class DownloadPdf:
    def __init__(self, *args, **kwargs):
        self.url = None
        self.file_name = None
        self.directory = kwargs.get("directory", "downloads")

    @staticmethod
    def build(directory=None):
        return DownloadPdf(directory=directory)

    def download_and_save_pdf(self, url, directory="downloads"):
        # Download the PDF file from the given URL
        original_filename = url.split("/")[-1]
        arxiv_number = original_filename.split(".pdf")[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        arxiv_dir = os.path.join(directory, arxiv_number)
        if not os.path.exists(arxiv_dir):
            os.makedirs(arxiv_dir)
        response = None
        full_path = os.path.join(arxiv_dir, original_filename)
        if os.path.exists(full_path):
            logger.info("PDF already downloaded: skipping")
            return
        logger.info(f"Downloading {arxiv_number} from {url}")
        try:
            response = requests.get(url)
            # Save the PDF file locally
            logger.info("Successfully downloaded PDf")
        except Exception as e:
            logger.error(f"Could not download PDF: {e}")
        with open(full_path, "wb") as file:
            file.write(response.content)
            file.close()
        metadata = {
            "arxiv_number": arxiv_number,
            "title": "",
            "pdf_filename": full_path,
            "images": {},
            "new_root": "",
            "pages": 0,
            "size": 0,
        }
        metadata_filename = os.path.join(arxiv_dir, "metadata.txt")
        with open(metadata_filename, "w") as f:
            f.write(json.dumps(metadata, indent=4))


class ReadPdf:
    def read_pdf(self, url):
        arxiv_dir, _, metadata = get_data_by_url(url)

        pdf_filepath = metadata.get("pdf_filename")
        new_root = ""
        with open(pdf_filepath, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_path = os.path.join(arxiv_dir, "raw.txt")
            image_num = 0
            if os.path.exists(text_path):
                logger.info("Text file for PDF already exists: skipping...")
                return
            with open(text_path, "w") as text_file:
                for page_num, page in enumerate(pdf_reader.pages):
                    metadata["pages"] += 1
                    # Write the content of the PDF to a text file
                    text = page.extract_text(0)
                    metadata["size"] += len(text)
                    if page_num == 0:
                        title = text.split("\n")[0]
                        metadata["title"] = title
                        new_sub_dir = title.replace(": ", "-").replace(" ", "_")
                        new_root = os.path.join("downloads", new_sub_dir)
                        metadata["new_root"] = new_root
                    text_file.write(text)

                    for i, image in enumerate(page.images):
                        image_num += 1
                        image_filename = f"image_{image_num}.png"
                        image_path = f"{new_root}/images/page_{page_num + 1}"
                        os.makedirs(image_path, exist_ok=True)
                        image_path = os.path.join(image_path, image_filename)
                        if not os.path.exists(image_path):
                            with open(image_path, "wb") as image_file:
                                image_file.write(image.data)
                                max_width = 1000
                                max_height = 1000
                                img = Image.open(image_path)
                                img.thumbnail((max_width, max_height), Image.LANCZOS)
                                img.save(image_path)
                        caption = self.extract_image_caption(metadata, text)

                        # Update image metadata
                        image_metadata = {
                            "caption": caption,
                            "image_path": image_path,
                        }
                        metadata["images"][image_filename] = image_metadata

            # Write metadata to a JSON file
            metadata_filename = os.path.join(arxiv_dir, "metadata.txt")
            with open(metadata_filename, "w") as f:
                f.write(json.dumps(metadata, indent=4, sort_keys=True))
                f.close()

    def delete_file(self, file_name, directory="downloads"):
        os.remove(file_name)

    def extract_image_caption(self, metadata, page_text):
        try:
            captions_so_far = [
                image.get("caption")
                for image in metadata.get("images").values()
                if image.get("caption")
            ]
            caption = ""
            next_figure_num = len(captions_so_far) + 1 if captions_so_far else 0
            attempts = 0
            while not caption and attempts < 5:
                # Define the pattern to match the caption starting with "Figure" and ending with a period
                pattern = r"(Figure {}:[^.]*(?:\.[^.]*){{0,1}})".format(
                    next_figure_num or attempts
                )
                # Search for the caption pattern in the text
                match = re.search(pattern, page_text)
                if match:
                    # Get the matched caption
                    candidate = match.group(1)
                    if candidate not in captions_so_far:
                        caption = candidate
                        print(caption)
                        return caption
                attempts += 1
            return ""
        except Exception as error:
            print(error)
            return None


class OpenAi:
    def __init__(self):
        self.temperature = 0.0
        self.model_35_4k = "gpt-3.5-turbo-0613"  # 4k tokens
        self.model_35_16k = "gpt-3.5-turbo-16k-0613"  # 16k tokens
        self.token_counter = tiktoken.encoding_for_model(self.model_35_16k)
        self.api_token = os.getenv("OPENAI_API_KEY")
        self.messages = []

    def get_tokens_in_prompt(self, total_prompt):
        if not self.token_counter:
            self.token_counter = tiktoken.encoding_for_model(self.model_35_16k)
        total_tokens = len(self.token_counter.encode(total_prompt))
        return total_tokens

    @backoff.on_exception(
        backoff.expo,
        exception=(
            APIError,
            OpenAIError,
            ServiceUnavailableError,
            APIConnectionError,
            Timeout,
            TryAgain,
        ),
        max_tries=5,
    )
    def call_openai(self, temperature=0.5, stream=False):
        try:
            res = openai.ChatCompletion.create(
                model=self.model_35_16k,
                messages=self.messages,
                temperature=temperature,
                stream=stream,
            )
            text_response = res.choices[0].message.content
            return text_response
        except RateLimitError:
            delay_secs = 5
            time.sleep(delay_secs)
        except Exception as err:
            logger.error(f"Unknown exception occured: {err}")
            return ""

    def safely_append_message(self, role, message):
        """Appends a given message to the chain while ensuring that context limit is not exceeded."""
        prev_messages = "".join([m["content"] for m in self.messages])
        total_tokens = self.get_tokens_in_prompt(prev_messages + message)
        logger.info(
            f"Current role: {role}. Total tokens in current Context: {total_tokens}"
        )
        # If total tokens exceed the limit, prune messages starting from oldest messages
        if total_tokens > 14000:
            while total_tokens > 7000 and self.messages:
                self.messages.pop(0)
                total_messages = "".join([m["content"] for m in self.messages])
                total_tokens = self.get_tokens_in_prompt(total_messages + message)
        # Actually append the message
        self.messages.append({"role": role, "content": message})

    def summarize_pdf_snippets(
        self, snippet, force_code=False, knowledge_lvl="under-graduate"
    ):
        text_summary = ""
        diagram_summary = ""
        code_summary = ""
        # Step 1: Summarize the snippet organically
        self.safely_append_message(
            "system",
            f"Summarize the snippet below using markdown syntax for a {knowledge_lvl} student. You should include brief intuitive examples to help build an abstract mental model of the key ideas."
            + "\n\n SNIPPET\n"
            + snippet,
        )
        text_summary = self.call_openai(temperature=0.5)
        if text_summary:
            self.safely_append_message("assistant", text_summary)

        self.safely_append_message(
            "system",
            "Provide a mermaid diagram in markdown syntax (e.g. ```mermaid ... ```) illustrating the concepts of this paper so far as you understand them.",
        )
        diagram_summary = self.call_openai(temperature=0.9)
        self.safely_append_message("assistant", diagram_summary)

        if force_code:
            self.safely_append_message(
                "system",
                "Create a Python class that illustrates the ideas that you've been shown so far to help the reader understand the more advanced ideas in this document.",
            )
            code_summary = self.call_openai(temperature=0.5)
            self.safely_append_message("assistant", code_summary)
            self.safely_append_message(
                "system",
                "Create a mermaid sequence diagram explaining the control flow of the code you provided in the previous message. Include labels and numbering using mermaid syntax so the variables and steps of the control flow are well understood.",
            )
            code_diagram = self.call_openai(temperature=0.9)
            self.messages.pop()
            self.safely_append_message(
                "system",
                "Show an example scenario with mocked log output of the code you generated, and then explain the hypothetical scenarios you mocked. Finally, also explain potential use cases of the code you generated in the previous message",
            )
            mock_scenario = self.call_openai(temperature=0.9)
            code_summary += f"\n\n{code_diagram}\n\n{mock_scenario}"

        # Step 3: Determine if a code summary can be created in Python.
        return text_summary, diagram_summary, code_summary

        ## NOTE: Streaming below
        # snippet_summary = ""
        # res = openai.ChatCompletion.create(
        #     model=self.model_35_16k,
        #     messages=messages,
        #     temperature=self.temperature,
        #     stream=True,
        # )

        # for chunk in res:
        #     delta = chunk["choices"][0]["delta"]
        #     if "content" in delta:
        #         snippet_summary += delta["content"]
        # return snippet_summary

    def expand_code_snippet(self, snippet):
        self.messages = []
        self.safely_append_message(
            "system",
            "Add more detailed logic to the Python code snippet below. You don't need to provide a summary after the expanded code, i will ask you for that in a subsequent message, just provide a more verbose version of the code already written."
            + "\n\n CODE SNIPPET\n"
            + snippet,
        )
        expanded_code = self.call_openai(temperature=0.9)
        self.safely_append_message("assistant", expanded_code)
        self.safely_append_message(
            "system",
            "Write a couple advanced unit tests with advanced mocked inputs for the code so it's clear how the interactions of the methods are expected to be used and interact with each other in real-world scenarios",
        )
        unit_tests = self.call_openai(temperature=0.5)
        return expanded_code, unit_tests


class SummarizeDoc(OpenAi):
    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    @staticmethod
    def build():
        return SummarizeDoc()

    def main(
        self,
        url,
        snippet_size=5000,
        force_code_summaries=False,
        knowledge_level="high-school",
    ):
        arxiv_dir, arxiv_number, metadata = get_data_by_url(url)

        rawtext_filename = os.path.join(arxiv_dir, "raw.txt")
        lite_filename = os.path.join(arxiv_dir, "lite.md")
        summary_filename = os.path.join(arxiv_dir, "summary.md")
        code_snippets_filename = os.path.join(arxiv_dir, "code_snippets.json")

        summary_file = open(summary_filename, "a")
        lite_file = open(lite_filename, "a")
        summary_file.write(f'# {metadata.get("title")}\n\n')
        summary_file.close()
        lite_file.write(f'{metadata.get("title")}\n\n')
        lite_file.close()

        logger.info(
            f"STARTING summary: \n  - arxiv id:{arxiv_number}\n  - title: {metadata.get('title')}"
        )

        snippet = ""
        token_count = 0
        code_snippets = []
        snippet_count = 1
        with open(rawtext_filename, "r") as f:
            for line in f:
                tokens_per_snippet = self.get_tokens_in_prompt(snippet + line)
                if tokens_per_snippet < snippet_size:
                    snippet += line
                    continue
                else:
                    if "." in line:
                        snippet += line.split(".")[0] + "."
                    logger.info(f"Fetching snippet summary of size: {token_count}")
                    (
                        text_summary,
                        diagram_summary,
                        code_summary,
                    ) = self.summarize_pdf_snippets(
                        f"{snippet_count}. \n{snippet}",
                        force_code_summaries,
                        knowledge_level,
                    )
                    logger.info(f"Snippet summarized successfully: processing summary")
                    lite_file = open(lite_filename, "a")
                    summary_file = open(summary_filename, "a")
                    # Find the corresponding image caption based on the "Figure X" part
                    figure_numbers = re.findall(r"Figure (\d+)", snippet)
                    for figure_number in list(set(figure_numbers)):
                        image_filename = f"image_{figure_number}.png"
                        image_data = metadata["images"].get(image_filename, {})
                        image_path = image_data.get("image_path")
                        if not image_data.get("caption"):
                            continue
                        if image_path:
                            img_text = '<div style="display: flex; flex-direction: column; gap: 25px; padding: 20px">\n'
                            img_text += f'<img src="/Users/tobiahrex/code/me/xivar-taj/{image_path}" style="max-width: 400px" />\n'
                            img_text += f'<p>{image_data.get("caption")}</p>\n'
                            img_text += "</div>\n"
                            summary_file.write(img_text)

                    if code_summary:
                        code_snippets.append(code_summary)
                    summary_file.write(f"{snippet_count}.\n{text_summary}" + "\n\n")
                    summary_file.write(diagram_summary + "\n\n")
                    summary_file.write(code_summary + "\n\n")
                    summary_file.close()
                    lite_file.write(f"{snippet_count}.\n" + text_summary + "\n\n")
                    lite_file.close()
                    snippet = snippet.split(".")[-1] + line
                    token_count = tokens_per_snippet
                    snippet = ""
                    text_summary = ""
                    diagram_summary = ""
                    code_summary = ""
                    snippet_count += 1
            f.close()
        if summary_file:
            summary_file.close()
        if lite_file:
            lite_file.close()
        code_snippets_file = open(code_snippets_filename, "w")
        code_snippets_file.write(json.dumps(code_snippets, indent=4))
        code_snippets_file.close()

        logger.info(
            f"FINISHED summary!\n  - arxiv id:{arxiv_number}\n  - title: {metadata.get('title')}"
        )

    def expand_code(self, url):
        arxiv_dir, _, meta_data = get_data_by_url(url)
        code_filename = os.path.join(arxiv_dir, "code_snippets.json")
        code_snippets = {}
        with open(code_filename, "r") as f:
            code_snippets = json.load(f)
        new_code_blocks = []
        for i, snippet in enumerate(code_snippets):
            new_snippet = {"code": snippet, "expansion": "", "summary": ""}
            logger.info(f"Fetching code expansion: #{i + 1}")
            code_expansion, code_summary = self.expand_code_snippet(snippet)
            new_snippet["expansion"] = code_expansion
            new_snippet["summary"] = code_summary
            new_code_blocks.append(new_snippet)
        expanded_code_filename = os.path.join(arxiv_dir, "code_explained.md")
        with open(expanded_code_filename, "w") as f:
            for i, block in enumerate(new_code_blocks):
                chunk = f"\n# {i + 1}. Code Block\n{block.get('code')}\n"
                f.write(chunk)
                chunk = f"## Details\n{block.get('expansion')}\n\n"
                f.write(chunk)
                chunk = f"## Summary\n{block.get('summary')}\n\n"
        logger.info("Successfully expanded all code snippets")


class XivarTaj:
    def __init__(self):
        pass

    @staticmethod
    def build():
        return XivarTaj()

    def main(self, jobs):
        for job in jobs:
            url = job.get("url")
            print("\n")
            logger.info(f"\n===== Starting Summary: '{url}' =====")
            # Download PDF (if not exists)
            d = DownloadPdf.build()
            d.download_and_save_pdf(url)

            # Read PDF & Save to Text'
            ReadPdf().read_pdf(url)

            # Summary of Text
            summarizer = SummarizeDoc.build()
            summarizer.main(
                url,
                job.get("snippet_size"),
                job.get("force_code_summaries"),
                job.get("knowledge_level"),
            )
            if job.get("expand_code"):
                summarizer.expand_code(url)
            logger.info("\n-------------")

            # Renaming final Directory
            arxiv_dir, _, metadata = get_data_by_url(url)
            new_root = metadata.get("new_root")
            old_root = arxiv_dir
            find_and_replace_doc_folder(new_root, old_root)


class ElevenLabs:
    VOICE_METADATA = "elevenlabs_voices.txt"
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/<voice-id>?optimize_streaming_latency=0"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ.get("ELEVENLABS_API_KEY", ""),
    }

    def __init__(self):
        pass

    @staticmethod
    def build():
        set_api_key(os.environ.get("ELEVENLABS_API_KEY", ""))
        return ElevenLabs()

    def tts(self, text="Hi my name is Toby, nice to meet you.", output_filename="output.mp3"):
        # audio = generate(text, voice="Adam", model="eleven_monolingual_v1")
        # play(audio)
        url = self.url.replace("<voice-id>", "pNInz6obpgDQGcFmaJgB")
        response = requests.post(
            url,
            headers=self.headers,
            json={
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.5,
                    "use_speaker_boost": True,
                },
            },
        )
        if response.ok:
            with open(output_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
        else:
            err_msg = dict(response.text).get("message", "")
            logger.error(f"Could not generate audio: {err_msg}")

    def get_voices(self):
        if not os.path.exists(self.VOICE_METADATA):
            _voices = voices()
            with open(self.VOICE_METADATA, "w") as f:
                metadata = {}
                for v in _voices:
                    data = dict(v)
                    metadata[data.get("name")] = {
                        "voice_id": data.get("voice_id"),
                        "category": data.get("category"),
                        "description": data.get("description", ""),
                        "preview_url": data.get("preview_url", ""),
                    }
                f.write(json.dumps(metadata, indent=4))

    def transcribe(self, folder):
        file_name = folder.split('/')[-1]
        audio_folder = os.path.join(folder, "audio")
        lite_summary = os.path.join(folder, 'lite.md')
        if os.path.exists(lite_summary):
            f = open(lite_summary, "r")
            text = f.read()

            chunk_size = 4000
            num_chunks = len(text) // chunk_size + 1

            if not os.path.exists(audio_folder):
                os.mkdir(audio_folder)

            for i in range(num_chunks):
                chunk_text = text[i * chunk_size: (i + 1) * chunk_size]
                audio_filename = os.path.join(folder, "audio", f"{file_name}_{i}.mp3")
                self.tts(chunk_text, audio_filename)


if __name__ == "__main__":
    XivarTaj.build().main(
        [
            # {"url": "https://arxiv.org/pdf/2304.03442.pdf", "expand_code": False},
            # {
            #     "url": "https://arxiv.org/pdf/2301.04589.pdf",
            #     "expand_code": True,
            #     "snippet_size": 1000,
            #     "force_code_summaries": True,
            # },
            # {
            #     "title": "Scaling Transformers to 1M tokens",
            #     "url": "https://arxiv.org/pdf/2304.11062.pdf",
            #     "expand_code": False,
            #     "snippet_size": 1000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "middle-school",
            # },
            # {
            #     "title": "Statistical analysis of chess games: space control and tipping points",
            #     "url": "https://arxiv.org/pdf/2304.11425.pdf",
            #     "expand_code": True,
            #     "snippet_size": 1000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "graduate",
            # },
            # {
            #     "title": "The centaur programmer - How Kasparov’s Advanced Chess spans over to the soware development of the future",
            #     "url": "https://arxiv.org/pdf/2304.11172.pdf",
            #     "expand_code": False,
            #     "snippet_size": 1000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "undergraduate",
            # },
            # {
            #     "title": "LongCoder: A Long-Range Pre-trained Language Model for Code Completion",
            #     "url": "https://arxiv.org/pdf/2306.14893.pdf",
            #     "expand_code": False,
            #     "snippet_size": 1000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "middle-school",
            # },
            # {
            #     "title": "EXPLORATION OF ALGORITHMIC TRADING STRATEGIES FOR THE BITCOIN MARKET",
            #     "url": "https://arxiv.org/pdf/2110.14936.pdf",
            #     "expand_code": False,
            #     "snippet_size": 1000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "high-school",
            # },
            # {
            #     "title": "BB Flow Chart",
            #     "url": "https://x.com/Black_Box_Trading_System.pdf",
            #     "expand_code": True,
            #     "snippet_size": 500,
            #     "force_code_summaries": True,
            #     "knowledge_level": "graduate",
            # },
            # {
            #     "title": "An intelligent algorithmic trading based on a risk-return reinforcement learning algorithm",
            #     "url": "https://arxiv.org/pdf/2208.10707.pdf",
            #     "expand_code": False,
            #     "snippet_size": 2000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "middle-school",
            # },
            # {
            #     "title": "An Application of Deep Reinforcement Learning to Algorithmic Trading",
            #     "url": "https://arxiv.org/pdf/2004.06627.pdf",
            #     "expand_code": False,
            #     "snippet_size": 2000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "middle-school",
            # },
            {
                "title": "An Automated Portfolio Trading System with Feature Preprocessing and Recurrent Reinforcement Learning",
                "url": "https://arxiv.org/pdf/2110.05299.pdf",
                "expand_code": False,
                "snippet_size": 2000,
                "force_code_summaries": True,
                "knowledge_level": "middle-school",
            },
            # {
            #     "title": "A Data Science Pipeline for Algorithmic Trading: A Comparative Study of Applications for Finance and Cryptoeconomics",
            #     "url": "https://arxiv.org/pdf/2206.14932",
            #     "expand_code": False,
            #     "snippet_size": 2000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "middle-school",
            # },
            # {
            #     "title": "CAUSALITY BETWEEN SENTIMENT AND CRYPTOCURRENCY PRICES",
            #     "url": "https://arxiv.org/pdf/2306.05803.pdf",
            #     "expand_code": False,
            #     "snippet_size": 2000,
            #     "force_code_summaries": True,
            #     "knowledge_level": "middle-school",
            # },
            {
                "title": "Random matrix theory and nested clustered portfolios on Mexican markets",
                "url": "https://arxiv.org/pdf/2306.05667.pdf",
                "expand_code": False,
                "snippet_size": 2000,
                "force_code_summaries": True,
                "knowledge_level": "middle-school",
            },
        ]
    )

    # ElevenLabs.build().transcribe('downloads/LongCoder-A_Long-Range_Pre-trained_Language_Model_for_Code_Completion')
