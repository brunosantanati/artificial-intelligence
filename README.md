# artificial-intelligence

## Links

### Ollama
[Ollama](https://ollama.com/)  
[Models](https://ollama.com/library)  
[How do I keep a model loaded in memory or make it unload immediately?](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-do-i-keep-a-model-loaded-in-memory-or-make-it-unload-immediately)  

### Hugging Face
[Hugging Face](https://huggingface.co/)  
[Models](https://huggingface.co/models)  

### Videos
[I Analyzed My Finance With Local LLMs](https://youtu.be/h_GTxRFYETY?si=jyL-aRR6_-2rNxsh)  
[O SEU PRÓPRIO CHATGPT! COMO FUNCIONA o MODELO de uma INTELIGÊNCIA ARTIFICIAL?](https://youtu.be/2gqWI9Z9DKM?si=ywOjDWR17vVr_AV8)  
[All You Need To Know About Running LLMs Locally](https://youtu.be/XwL_cRuXM2E?si=7s1cS8TC9q2ySGbz)  
[Run your own AI (but private)](https://youtu.be/WxYC9-hBM_g?si=Byiye1lI_hMuk5jM)  

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
