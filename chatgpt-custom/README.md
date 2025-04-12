### Original project:  
[Using ChatGPT with YOUR OWN Data. This is magical. (LangChain OpenAI API)](https://www.youtube.com/watch?v=9AXP7tCI9PI)  
[GitHub repository](https://github.com/techleadhd/chatgpt-retrieval)  

### How to run chatgpt-simpler.py

Install these dependencies:  
<code>pip install openai</code>  
<code>pip install langchain</code>  
<code>pip install langchain-community</code>  
<code>pip install langchain-openai</code>  

Set OPENAI_API_KEY as an environment variable containing the OpenAI API Key.  

Run the script:  
<code>python3 chatgpt-simpler.py "who is George Washington"</code>  

### How to run chatgpt-simpler-local.py

Download mistral-7b-instruct-v0.1.Q4_0.gguf and put it inside models folder:
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main

Install these dependencies:
<code>pip install langchain faiss-cpu sentence-transformers gpt4all</code>

Run the script:
python3 chatgpt-simpler-local.py "resuma o texto"
