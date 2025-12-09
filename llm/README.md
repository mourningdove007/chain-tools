# Ollama Client

This client allows us to provide context to a running instance of an [Ollama](https://ollama.com/) LLM. The following process describes how our locally running LLM file analyzer is used.

Install the virtual environment.

```
python3 -m venv venv
```

Activate the environment and install the requirements.

```
source venv/bin/activate

pip install -r requirements.txt
```

### File Analyzer

Analyzes the contents of a file and saves a summary to `rust_code_analysis.txt`.

```
python file_analyzer.py my_directory
```
