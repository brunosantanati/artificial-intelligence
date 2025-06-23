# artificial-intelligence

## Links

### Ollama
[Ollama](https://ollama.com/)  
[Models](https://ollama.com/library)  
[How do I keep a model loaded in memory or make it unload immediately?](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-do-i-keep-a-model-loaded-in-memory-or-make-it-unload-immediately)  

### Hugging Face
[Hugging Face](https://huggingface.co/)  
[Models](https://huggingface.co/models)  

### Articles

[AI 2027](https://ai-2027.com/)  
[OpenAI Codex CLI – Getting Started](https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started)  
[Blog post about Little Language Lessons](https://blog.google/outreach-initiatives/education/little-language-lessons/)  

### Tools

[CrewAI](https://www.crewai.com/)  
[DeepSeek](https://www.deepseek.com/en)  
[Manus](https://manus.im/)  
[llama.cpp](https://github.com/ggml-org/llama.cpp)  
[JNI to integrate with llama.cpp](https://pt.m.wikipedia.org/wiki/Java_Native_Interface)  
[ClaudeAI](https://claude.ai/)  
[NotebookLM](https://notebooklm.google.com)  
[LindyAI](https://www.lindy.ai/)  
[CursorAI](https://www.cursor.com/)  
[Grok](https://grok.com/)  
[Little Language Lessons](https://labs.google/lll/en)  
[Jules](https://jules.google/)  
[Flux AI](https://flux-ai.io/)  
[Stability AI](https://stability.ai/)  
[Midjourney](https://www.midjourney.com/home)  
[DALLE 3](https://openart.ai/home)  
[DALLE 2](https://openai.com/index/dall-e-2/)  
[Elevenlabs](https://elevenlabs.io/)  

### Videos
[I Analyzed My Finance With Local LLMs](https://youtu.be/h_GTxRFYETY?si=jyL-aRR6_-2rNxsh)  
[O SEU PRÓPRIO CHATGPT! COMO FUNCIONA o MODELO de uma INTELIGÊNCIA ARTIFICIAL?](https://youtu.be/2gqWI9Z9DKM?si=ywOjDWR17vVr_AV8)  
[All You Need To Know About Running LLMs Locally](https://youtu.be/XwL_cRuXM2E?si=7s1cS8TC9q2ySGbz)  
[Run your own AI (but private)](https://youtu.be/WxYC9-hBM_g?si=Byiye1lI_hMuk5jM)  
[Train ChatGPT On Your Data (Easy Method)](https://www.youtube.com/watch?v=y9Gi3UgNA3E)  
[How to Use ChatGPT with Your Own Data](https://www.youtube.com/watch?v=tCdy-ksJGl4)  
[How to Train ChatGPT with Your Own Data](https://www.youtube.com/watch?v=-iuEVOFyZj8)  
[How to train ChatGPT on your own data - (2024)](https://www.youtube.com/watch?v=BK2rcC6zEaU)  
[How to Train ChatGPT on Your Own Data - Build a Custom AI Chatbot](https://www.youtube.com/watch?v=LcG919C4UeU)  
[Using ChatGPT with YOUR OWN Data. This is magical. (LangChain OpenAI API)](https://www.youtube.com/watch?v=9AXP7tCI9PI) - [GitHub repo](https://github.com/techleadhd/chatgpt-retrieval)  
[TESTAMOS O CODEX CLI DA OPENAI (AGORA FAZ PARTE DA NOSSA STACK)](https://www.youtube.com/watch?v=X3Igp8NX1YI)  

## Commands
```
Install Ollama on Linux:
curl -fsSL https://ollama.com/install.sh | sh

Check installation / version:
ollama -v

List models:
ollama list

Pull mistral model:
ollama pull mistral

Run mistral model:
ollama run mistral

Show help:
ollama help

Call ollama API to unload a model immediately:
curl http://localhost:11434/api/generate -d '{"model":"mistral", "keep_alive":0}'

ollama help output:
--------------------------------------
Large language model runner

Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.
--------------------------------------
```
