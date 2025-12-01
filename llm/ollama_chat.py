import ollama
import sys

# --- ANSI Color Codes ---
RED = '\033[91m'     # Bright Red for errors
GREEN = '\033[92m'   # Bright Green for success
YELLOW = '\033[93m'  # Bright Yellow for warnings/titles
CYAN = '\033[96m'    # Bright Cyan for the analysis header
BOLD = '\033[1m'     # Bold text
ENDC = '\033[0m'     # Reset color/style
# ------------------------

def analyze_piped_input(model_name="llama3.2"):

    try:
        error_input = sys.stdin.read().strip()
    except Exception as e:
        print(f"❌ Error reading piped input: {e}", file=sys.stderr)
        return

    if not error_input:
        print(
            "\n✅ No input received (tests likely passed or ran cleanly). No analysis needed.",
            file=sys.stderr,
        )
        return

    try:
        client = ollama.Client(host="http://localhost:11434")
    except Exception as e:
        print(f"❌ Ollama Connection Error: {e}", file=sys.stderr)
        print(
            "Please ensure the Ollama server is running on http://localhost:11434.",
            file=sys.stderr,
        )
        return

    initial_instruction = (
        "Analyze the following Rust test output, focusing only on failures or errors. "
        "Provide a concise explanation of the root cause and suggest the most likely fix. "
        "Ignore all warnings and only include the analysis if there is a failure. "
        "If the output indicates all tests passed successfully, you must ONLY respond 'All tests passed.'. "
        "Discuss any areas of concern including file paths and line numbers."
        "Here is the full test output:\n\n"
    )
    full_prompt = initial_instruction + error_input

    print("\nAnalyzing test output...", file=sys.stderr)

    try:
        response = client.generate(model=model_name, prompt=full_prompt, stream=False)

        llm_analysis = response["response"]

        print(f"{GREEN if "All tests passed" in llm_analysis else RED}\n========================\n")
        print(llm_analysis)
        print("==========================\n")

    except ollama.RequestError as e:
        print(f"\n❌ LLM Request Error: {e}", file=sys.stderr)


if __name__ == "__main__":

    MODEL = "llama3.2"
    analyze_piped_input(MODEL)
