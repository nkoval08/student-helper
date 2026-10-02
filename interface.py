RESET = "\033[0m"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

def show_title(title):
    print()
    print(CYAN + "=" * 40 + RESET)
    print(CYAN + f"        {title}" + RESET)
    print(CYAN + "=" * 40 + RESET)

def show_success(message):
    print(GREEN + f"✅ {message}" + RESET)

def show_error(message):
    print(RED + f"❌ {message}" + RESET)

def show_warning(message):
    print(YELLOW + f"⚠️ {message}" + RESET)

def show_info(message):
    print(BLUE + f"ℹ️ {message}" + RESET)

def pause():
    input(YELLOW + "\nНажмите Enter, чтобы продолжить..." + RESET)