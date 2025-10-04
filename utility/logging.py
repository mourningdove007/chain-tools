
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
LIGHT_BLUE = '\033[94m'
LIGHT_PINK = '\033[95m'

BOLD = '\033[1m'

RESET = '\033[0m' 

def print_red(message: str):
    print(f"{RED}{message}{RESET}")

def print_green(message: str):
    print(f"{GREEN}{message}{RESET}")

def print_yellow(message: str):
    print(f"{YELLOW}{message}{RESET}")

def print_info(message: str):
    print(f"{LIGHT_PINK}{message}{RESET}")

def print_whale(message: str):
    print(f"{LIGHT_BLUE}{message}{RESET}")

if __name__ == "__main__":

    print_red("ERROR")
    print_green("SUCCESS")
    print_yellow("WARNING")
    print_info("INFO")
    print_whale("WHALE")