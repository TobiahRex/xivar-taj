import os
import requests
import PyPDF2
import json
import re
from PIL import Image
from dotenv import load_dotenv
import logging
from datetime import datetime as dt
import openai
import tiktoken

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DownloadPdf:
    def __init__(self, *args, **kwargs):
        self.url = None
        self.file_name = None
        self.directory = kwargs.get('directory', 'downloads')

    @staticmethod
    def build(directory=None):
        return DownloadPdf(directory=directory)

    def download_and_save_pdf(self, url, directory="downloads"):
        # Download the PDF file from the given URL
        file_name = url.split('/')[-1]
        file_root = file_name.split('.pdf')[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        sub_dir = os.path.join(directory, file_root)
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
        response = None
        full_path = os.path.join(sub_dir, file_name)
        if not os.path.exists(full_path):
            logger.info(f"Downloading {file_name} from {url}")
            response = requests.get(url)
            # Save the PDF file locally
            with open(full_path, 'wb') as file:
                file.write(response.content)
                file.close()

class ReadPdf:

    def read_pdf(self, folder_name, directory="downloads"):
        pdf_filename = ''
        for file in os.listdir(os.path.join(directory, folder_name)):
            if file.endswith('.pdf'):
                pdf_filename = file
                break
        sub_dir = folder_name.split('.pdf')[0]
        file_path = os.path.join(directory, sub_dir, pdf_filename)
        # Read the downloaded PDF file line by line
        old_root = os.path.join(directory, sub_dir)
        new_root = ''
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            metadata = {
                'images': {},
                'title': '',
                'pages': 0,
                'size': 0,
                'pdf_filename': pdf_filename,
            }
            text_path = os.path.join(directory, sub_dir, pdf_filename.replace('.pdf', '.txt'))
            image_num = 0
            with open(text_path, 'w') as text_file:
                for page_num, page in enumerate(pdf_reader.pages):
                    metadata['pages'] += 1
                    # Write the content of the PDF to a text file
                    text = page.extract_text(0)
                    metadata['size'] += len(text)
                    if page_num == 0:
                        title = text.split('\n')[0]
                        metadata['title'] = title
                        new_sub_dir = title.replace(': ', '-').replace(' ', '_')
                        new_root = os.path.join(directory, new_sub_dir)
                        self.find_and_replace_doc_folder(new_root, old_root)
                    text_file.write(text)

                    for i, image in enumerate(page.images):
                        image_num += 1
                        image_filename = f'image_{image_num}.png'
                        image_path = f"{new_root}/images/page_{page_num + 1}"
                        os.makedirs(image_path, exist_ok=True)
                        image_path = os.path.join(image_path, image_filename)
                        if not os.path.exists(image_path):
                            with open(image_path, 'wb') as image_file:
                                image_file.write(image.data)
                                max_width = 1000
                                max_height = 1000
                                img = Image.open(image_path)
                                img.thumbnail((max_width, max_height), Image.LANCZOS)
                                img.save(image_path)
                        caption = self.extract_image_caption(metadata, text)

                        # Update image metadata
                        image_metadata = {
                            'caption': caption,
                            'image_path': image_path,
                        }
                        metadata['images'][image_filename] = image_metadata

            # Write metadata to a JSON file
            metadata_file = os.path.join(new_root, 'metadata.txt')
            with open(metadata_file, 'w') as f:
                f.write(json.dumps(metadata, indent=4, sort_keys=True))
                f.close()
        return new_sub_dir

    def delete_file(self, file_name, directory="downloads"):
        os.remove(file_name)


    def extract_image_caption(self, metadata, page_text):
        try:
            captions_so_far = [image.get('caption') for image in metadata.get('images').values() if image.get('caption')]
            caption = ''
            next_figure_num = len(captions_so_far) + 1 if captions_so_far else 0
            attempts = 0
            while not caption and attempts < 5:
                # Define the pattern to match the caption starting with "Figure" and ending with a period
                pattern = r'(Figure {}:[^.]*(?:\.[^.]*){{0,1}})'.format(next_figure_num or attempts)
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
            return ''
        except Exception as error:
            print(error)
            return None


    @staticmethod
    def find_and_replace_doc_folder(new_root, old_root):
        if new_root != old_root:
            if os.path.exists(old_root):
                os.rename(old_root, new_root)

class OpenAi:
    def __init__(self):
        self.temperature = 0.0
        self.model_35_4k = 'gpt-3.5-turbo-0613' # 4k tokens
        self.model_35_16k = 'gpt-3.5-turbo-16k-0613' # 16k tokens
        self.token_counter = tiktoken.encoding_for_model(self.model_35_16k)
        self.api_token = os.getenv('OPENAI_API_KEY')
        self.initial_instructions = """
            INSTRUCTIONS:
            - You are a going to summarize, extract, and modify snippets of text into a markdown file using markdown syntax. The snippets you will be shown all be individual parts of a larger text document.
            - The snippets will be around 14000 tokens. Your summary should be between 6000-7000 tokens (not including the code snippets you will be asked to produce, and diagrams you will be asked to produce)
            - All of your summaries should be written for a high-school audience to understand.
            - You can assume that your high-school audience are Python Experts.
            - You should include at least one diagram in each summary you produce. You can use the following types of diagrams:
                1. mermaid sequence diagrams to explain how code works
                2. meremaid state diagrams to explain how ideas flow together
            - You should include one of these diagrams for each snippet you are given in markdown friendly mermaid syntax.
                * this is a GOOD Example of a mermaid diagram in the markdown friendly syntax:
                    - ```mermaid
                        sequenceDiagram
                            Alice->>John: Hello John, how are you?
                            John-->>Alice: Great!
                            Alice-)John: See you later!
                        ```
                    - ```mermaid
                        sequenceDiagram
                            box Purple Alice & John
                            participant A
                            participant J
                            end
                            box Another Group
                            participant B
                            participant C
                            end
                            A->>J: Hello John, how are you?
                            J->>A: Great!
                            A->>B: Hello Bob, how is Charly ?
                            B->>C: Hello Charly, how are you?
                      ```
                * this is a BAD example of a mermaid diagram:
                    - ![Sequence Diagram](sequence_diagram.png) <- DO NOT DO THIS
                    - ![State Diagram](state_diagram.png) <- DO NOT DO THIS
            - When you produce a summary you should preserve any sectional numbering information that is present in the original document. For example
                * if you see ```1.1.1 <original snippet text>``` in the original document, you should preserve that in your summary but you should apply inuitive markdown syntax.
            - Some of these documents will have chunks of code in them in different languages; including python, and others. Some documents will have psuedo code that you will need to convert to python.
            - Some of these documents will have extremely complex and long mathematical formulas that were written for Latex presentation, however when i give them to you, they will be mutated and you will need to convert these formulas back into Markdown-Ready Latex syntax AND python code. Here's an example of the Latex syntax you will need to use for markdown.
                * $ \sum_{i=1}^n i = \\frac{n(n+1)}{2} $
                * Regarding Python code you should create snippets ready for Markdown presentation that look like this:
                ```python
                 <python code here>
                ```
            - The Python code you produce is meant to translate the ideas in the original document into code that can be run and undestood by a python expert. You should not be trying to produce the most efficient code possible. You should be trying to produce the most readable code possible that effectively demonstrates the ideas in the document or snippet you are shown.dt
            - Occassionally you will be given a snippet that ends with partial code, so you should wait until you see the entire code snippet before you start writing your summary and the new Python code that goes with it.
        """
        self.messages = [
            {
                "role": "system",
                "content": self.initial_instructions
            }
        ]

    def get_tokens_in_prompt(self, total_prompt):
        if not self.token_counter:
            self.token_counter = tiktoken.encoding_for_model(self.model)
        total_tokens = len(self.token_counter.encode(" ".join(total_prompt)))
        return total_tokens

    def safely_append_message(self, role, message):
        """Appends a given message to the chain while ensuring that context limit is not exceeded."""
        total_messages = [m["content"] for m in self.messages]
        total_messages.append(message)
        total_tokens = self.get_tokens_in_prompt(total_messages)
        logger.info(
            f"Current role: {role}. Total tokens in current Context: {total_tokens}"
        )
        # If total tokens exceed the limit, prune messages starting from oldest messages
        if total_tokens > 15000:
            while total_tokens > 5000:
                self.messages.pop(0)
                total_messages = [m["content"] for m in self.messages]
                total_tokens = self.get_tokens_in_prompt(total_messages)
            for i, m in enumerate(self.messages):
                if m["role"] == "system" and m["content"] == self.initial_instructions:
                    self.messages.pop(i)
                    break
            self.messages.append({"role": "system", "content": self.initial_instructions})
        # Actually append the message
        self.messages.append({"role": role, "content": message})


    def summarize(self, snippet):
        messages = [
            {
                "role": "system",
                "content": self.initial_instructions + "\n\n SNIPPET ```" + snippet + "```"
            }
        ]
        ### NOTE: Non-streaming below
        res_1 = openai.ChatCompletion.create(
            model=self.model_35_16k,
            messages=messages,
            temperature=self.temperature,
            stream=False,  # Set streaming to False
        )

        text_snippet_summary = res_1.choices[0].message.content
        messages = [
            {
                "role": "system",
                "content": "Convert this snippet to python class that demonstrates the outlined behavior with an accompanied mermaid sequence diagram" + "\n\n SNIPPET ```" + snippet + "```"
            }
        ]
        res_2 = openai.ChatCompletion.create(
            model=self.model_35_16k,
            messages=messages,
            temperature=self.temperature,
            stream=False,  # Set streaming to False
        )
        code_snippet_summary = res_2.choices[0].message.content

        return text_snippet_summary, code_snippet_summary


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

class SummarizeDoc(OpenAi):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.dir_name = kwargs.get('dir_name', None)
        self.metadata = self.load_metadata()

    @staticmethod
    def build(dir_name):
        return SummarizeDoc(dir_name=dir_name)

    def load_metadata(self):
        meta_filepath = os.path.join(self.dir_name, 'metadata.txt')
        if os.path.exists(meta_filepath):
            with open(meta_filepath, 'r') as meta_file:
                metadata = json.load(meta_file)
            return metadata
        return {}

    def main(self):
        meta_filepath = os.path.join(self.dir_name, 'metadata.txt')
        meta_file = None
        if os.path.exists(meta_filepath):
            meta_file = open(meta_filepath, 'r')
        meta_data = json.loads(meta_file.read())

        rawtext_filepath = ''
        for file in os.listdir(self.dir_name):
            if file.endswith('.txt') and 'metadata' not in file:
                rawtext_filepath = os.path.join(self.dir_name, file)
                break

        summary_filepath = os.path.join(self.dir_name, 'summary.md')
        summary_file = open(summary_filepath, 'a')
        summary_file.write(f'# {self.metadata.get("title")}\n\n')
        summary_file.close()

        snippet = ''
        token_count = 0
        ideal_token_size = int(meta_data.get('size') / (3 * 10))
        with open(rawtext_filepath, 'r') as f:
            for line in f:
                tokens_per_line = self.get_tokens_in_prompt(line)
                if token_count + tokens_per_line < min(ideal_token_size, 15000):
                    token_count += tokens_per_line
                    snippet += line
                    continue
                else:
                    text_summary, code_summary = self.summarize(snippet)
                    summary_file = open(summary_filepath, 'a')
                    # Find the corresponding image caption based on the "Figure X" part
                    figure_numbers = re.findall(r'Figure (\d+)', snippet)
                    for figure_number in list(set(figure_numbers)):
                        image_filename = f'image_{figure_number}.png'
                        image_data = self.metadata['images'].get(image_filename, {})
                        image_path = image_data.get('image_path')
                        if not image_data.get('caption'):
                            continue
                        if image_path:
                            img_text = '<div style="display: flex; flex-direction: column; gap: 25px; padding: 20px">\n'
                            img_text += f'<img src="/Users/trex/code/me/xivar-taj/{image_path}" />\n'
                            img_text += f'<p>{image_data.get("caption")}</p>\n'
                            img_text += '</div>\n'
                            summary_file.write(img_text)

                    summary_file.write(text_summary + '\n\n\n')
                    summary_file.write(code_summary + '\n\n')
                    summary_file.close()
                    snippet = snippet.split('.')[-1] + line
                    token_count = tokens_per_line
                    snippet = ''
                    summary = ''
            f.close()
        if meta_file:
            meta_file.close()
        if summary_file:
            summary_file.close()


class XivarTaj:
    def __init__(self):
        pass

    @staticmethod
    def build():
        return XivarTaj()

    def main(self, urls):
        for url in urls:
            # Download PDF
            d = DownloadPdf.build()
            d.download_and_save_pdf(url)
            file_to_read = url.split('/')[-1].split('.pdf')[0]

            # Read PDF & Save to Text'
            folder_name = ReadPdf().read_pdf(file_to_read)
            # folder_name = "Generative_Agents-Interactive_Simulacra_of_Human_Behavior"
            # folder_name = "Scaling_Transformer_to_1M_tokens_and_beyond_with"

            # Summary of Text
            summary = SummarizeDoc.build(os.path.join('downloads', folder_name))
            summary.main()

if __name__ == '__main__':
    XivarTaj.build().main([
        'https://arxiv.org/pdf/2304.11062.pdf',
        'https://arxiv.org/pdf/2301.04589.pdf',
    ])