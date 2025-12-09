import ollama
import sys
import os


RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"


def analyze_directory(
    directory_path,
    model_name="llama3.2",
    output_filename="ollama_analysis.txt",
    context="context",
):

    print(
        f"{CYAN}preparing to analyze files in directory: '{directory_path}'...",
        file=sys.stderr,
    )

    if not os.path.isdir(directory_path):
        print(
            f"{CYAN}error: directory not found at '{directory_path}'. exiting.",
            file=sys.stderr,
        )
        return

    if os.path.exists(output_filename):
        print(
            f"{CYAN}warning: output file '{output_filename}' already exists and will be overwritten.",
            file=sys.stderr,
        )

    try:
        client = ollama.Client(host="http://localhost:11434")
    except Exception as e:
        print(f"{RED}ollama connection error: {e}", file=sys.stderr)
        print(
            f"{CYAN}please ensure the ollama server is running on http://localhost:11434.",
            file=sys.stderr,
        )
        return

    initial_instruction = (
        "Here is the context: "
        "Context Begins Here\n\n" + str(context) + "\n\n" + "Context Ends Here\n\n"
        "Answer only by giving a title of what you think the file name should be."
        "Here is the full file:\n\n"
    )

    total_analysis = ""
    file_count = 0

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if not file_name.endswith((".rs")):
                continue

            file_count += 1
            print(
                f"{CYAN}  -> analyzing file {file_count}: '{file_path}'...",
                file=sys.stderr,
            )

            try:

                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                full_prompt = initial_instruction + file_content

                response = client.generate(
                    model=model_name, prompt=full_prompt, stream=False
                )
                llm_analysis = response["response"]

                file_output_block = (
                    f"{CYAN}## analysis for: `{file_path}`\n"
                    f"{CYAN}---"
                    f"{CYAN}{llm_analysis.strip()}\n\n"
                )

                print(f"{CYAN}{file_output_block}")

                total_analysis += file_output_block

            except ollama.RequestError as e:
                error_block = f"{CYAN}## analysis failed for: `{file_path}`\nerror: llm request error: {e}\n\n"
                total_analysis += error_block
                print(
                    f"{CYAN}  -> llm request error for '{file_path}': {e}",
                    file=sys.stderr,
                )
            except Exception as e:
                error_block = f"{CYAN}## analysis failed for: `{file_path}`\nerror: could not read file or unexpected error: {e}\n\n"
                total_analysis += error_block
                print(
                    f"{CYAN}  -> warning/error for '{file_path}': {e}", file=sys.stderr
                )
                continue

    if total_analysis:
        final_report = (
            f"{CYAN}# code analysis report ({model_name})\n\n"
            f"{CYAN}analysis completed for {file_count} rust files.\n\n"
            f"{CYAN}================================================\n\n"
        )
        final_report += total_analysis

        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_report)

        print(
            f"{GREEN}\nanalysis complete. output for {file_count} files saved to '{output_filename}'.",
            file=sys.stderr,
        )
    else:
        print(f"{CYAN}no rust files found or analyzed. exiting.", file=sys.stderr)

    return final_report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{CYAN}usage: python analyzer.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    DIRECTORY_TO_ANALYZE = sys.argv[1]
    MODEL = "llama3.2"
    OUTPUT_FILE = "rust_code_analysis.txt"

    analyze_directory(DIRECTORY_TO_ANALYZE, MODEL, OUTPUT_FILE)
