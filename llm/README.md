# Ollama Client

This client allows us to provide context to a running instance of an Ollama LLM.

Install the virtual environment.

```
python3 -m venv venv
```

Activate the environment and install the requirements.

```
source venv/bin/activate

pip install -r requirements.txt
```


### Analyze Test Output of Rust Example

This mode starts a continuous chat session using the default model (llama3 or the one specified in the script).

```
cargo test myTest.rs -- --nocapture 2>&1 | python ollama_chat.py
```
