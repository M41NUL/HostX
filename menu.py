import os
import sys
import webbrowser
from utils import C, print_line, clear
from config import TELEGRAM_CHANNEL, TOOL_NAME, VERSION, AUTHOR, OWNER, GITHUB_URL, TELEGRAM_GROUP, EMAIL, YOUTUBE, WHATSAPP, TELEGRAM, COPYRIGHT

# ============================================
# MENU
# ============================================

MENU_ITEMS = [
    ("1", "🌐  Start Local Server",   "server"),
    ("2", "👤  Developer Info",        "devinfo"),
    ("3", "❌  Exit",                  "exit"),
]


def show_menu():
    w = 50
    border = C.CYAN

    print(f"{border}╔{'═' * w}╗{C.RESET}")

    title = f"{C.BOLD}{C.YELLOW}  MENU{C.RESET}"
    _box_row(title, w, border)

    print(f"{border}╠{'═' * w}╣{C.RESET}")

    for num, label, _ in MENU_ITEMS:
        content = f"  {C.CYAN}[{num}]{C.RESET}  {C.WHITE}{label}{C.RESET}"
        _box_row(content, w, border)

    print(f"{border}╚{'═' * w}╝{C.RESET}")

    print(f"\n{C.YELLOW}  Select option: {C.RESET}", end="")


def _box_row(content, width, border_color):
    import re
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    clean = ansi_escape.sub('', content)
    padding = width - len(clean)
    if padding < 0:
        padding = 0
    print(f"{border_color}│{C.RESET}{content}{' ' * padding}{border_color}│{C.RESET}")


def handle_menu(choice):
    from server import start_server

    for num, label, action in MENU_ITEMS:
        if choice == num:
            if action == "server":
                start_server()
            elif action == "devinfo":
                show_dev_info()
            elif action == "exit":
                do_exit()
            return

    print(f"\n{C.RED}[✗]{C.RESET} Invalid option. Try again.\n")
    input(f"{C.DIM}Press Enter...{C.RESET}")


def show_dev_info():
    clear()
    w = 50
    border = C.CYAN
    label  = C.YELLOW + C.BOLD
    val    = C.WHITE

    def row(lbl, value):
        content = f"  {label}{lbl:<12}{C.RESET}{val}{value}{C.RESET}"
        _box_row(content, w, border)

    def spacer():
        _box_row("", w, border)

    print(f"\n{border}╔{'═' * w}╗{C.RESET}")
    _box_row(f"{C.BOLD}{C.CYAN}  Developer Information{C.RESET}", w, border)
    print(f"{border}╠{'═' * w}╣{C.RESET}")

    spacer()
    row("Name    :", AUTHOR)
    row("Brand   :", OWNER)
    spacer()
    row("GitHub  :", GITHUB_URL)
    row("TG Dev  :", f"t.me/{TELEGRAM.replace('t.me/', '')}")
    row("Channel :", TELEGRAM_CHANNEL)
    row("Group   :", TELEGRAM_GROUP)
    row("Email   :", EMAIL)
    row("YouTube :", YOUTUBE)
    row("WhatsApp:", WHATSAPP)
    spacer()

    print(f"{border}╠{'═' * w}╣{C.RESET}")
    _box_row(f"  {C.DIM}{COPYRIGHT}{C.RESET}", w, border)
    print(f"{border}╚{'═' * w}╝{C.RESET}\n")

    input(f"{C.DIM}  Press Enter to go back...{C.RESET}")


def do_exit():
    clear()
    print(f"\n{C.CYAN}  Redirecting to Telegram Channel...{C.RESET}")
    print(f"  {C.YELLOW}{TELEGRAM_CHANNEL}{C.RESET}\n")

    try:
        webbrowser.open(TELEGRAM_CHANNEL)
    except Exception:
        pass

    import time
    time.sleep(2)

    print(f"{C.GREEN}  Thanks for using {C.BOLD}{TOOL_NAME}{C.RESET}{C.GREEN}!{C.RESET}")
    print(f"  {C.DIM}~ {OWNER}{C.RESET}\n")
    sys.exit(0)
