import ollama
import sys


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
        "If the output indicates all tests passed successfully, you must say 'All tests passed.'. "
        "Here is the full test output:\n\n"
    )
    full_prompt = initial_instruction + error_input

    print("\nAnalyzing test output...", file=sys.stderr)

    try:
        response = client.generate(model=model_name, prompt=full_prompt, stream=False)

        llm_analysis = response["response"]

        print("\n================================================================\n")
        print(llm_analysis)
        print("==================================================================\n")

    except ollama.RequestError as e:
        print(f"\n❌ LLM Request Error: {e}", file=sys.stderr)


if __name__ == "__main__":

    MODEL = "llama3.2"
    analyze_piped_input(MODEL)
