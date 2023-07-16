# _Xivar_-Taj
### A simple Python script to extract the key ideas from an arxiv.org PDF file and...
- generate a mental model of the information (mermaid)
- with generative psuedo code (python)
- and example code snippets
- and Text-to-Speech audio summary to boot. (eleven labs)

<img src="https://imgur.com/Khy8LRI.png" style="width: 400px">

Doctor Strange had "Kamar Taj" a temple & library full of wisdom and magical powers bound up in books. We mortal humans have _Xivar-Taj_, sourcing the magical powers of arXiv.org. 🪄🎩🐰  This simple python script I hacked together on a plane ride from San Francisco to Tokyo (16hr) to prove to myself that LLM's have introduced a new workflow for learning that lets us concentrate on the information rather than the medium.


<img src="https://imgur.com/J15913R.png" style="width: 500px">



## Control Flow
The control flows in the `main.py` file executes are as follows.
1. Download the PDF from arXiv.org
2. Extract the text from the PDF
3. Extract any found images from the PDF
4. Iterate through the text using a sliding window of 16k tokens (GPT 3.5)
5. For Each sliding window chunk size
    1. summarize the data
    2. generate a Mermaid syntax diagram providing a Mental Model of the information
    3. generate psuedo Python code classes that express the key ideas in the window if appropriate.
    4. generate a series of example usage code snippets that express the key ideas in the window if appropriate.
6. Append generated chunks into a single file.
    1. If there's an image reference given the current window chunk, insert the image from those found in the PDF.
7. Finally summarize the document using the Eleven Labs API in a Text-to-Speech format.

Done.


## Why?
I absolutely love learning. I was fortunate enough to take my time learning to learn, rather than drinking from the academic fire-hose by going to college directly out of High-School. Instead I decided I wanted more time to learn what I liked to learn. I eventually came upon a simple truth;
> Learning is nothing more than building mental models, then applying that mental model to a particular skill-set to actualize your mental model into physical reality.

So, what better way to systematically learn than to build a mental model generating machine, and generate example code snippets to apply the mental model to a particular skill-set? It's like Neo jacking into the Matrix and learning Kung-Fu in 5 seconds.

<img src="https://imgur.com/eMiJ5nQ.png" style="width: 500px">