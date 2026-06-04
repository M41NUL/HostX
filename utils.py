import os
import sys

# ============================================
# ANSI COLOR CODES
# ============================================

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Foreground
    BLACK   = "\033[30m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    # Background
    BG_BLACK  = "\033[40m"
    BG_BLUE   = "\033[44m"
    BG_CYAN   = "\033[46m"


def clear():
    os.system("clear")


def pause(msg="Press Enter to continue..."):
    input(f"\n{C.DIM}{msg}{C.RESET}")


def print_line(char="─", length=52, color=C.CYAN):
    print(f"{color}{char * length}{C.RESET}")


def center_text(text, width=52):
    return text.center(width)


def box_line(content, width=50, border_color=C.CYAN, text_color=C.WHITE):
    """Print a single box row: │ content │"""
    # Strip ANSI for length calculation
    import re
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    clean = ansi_escape.sub('', content)
    padding = width - len(clean)
    if padding < 0:
        padding = 0
    print(f"{border_color}│{C.RESET} {text_color}{content}{' ' * padding}{border_color}│{C.RESET}")


def open_url(url):
    """Open URL in Termux using termux-open-url, fallback to webbrowser."""
    import subprocess
    import webbrowser
    try:
        result = subprocess.run(["termux-open-url", url], timeout=5)
        if result.returncode != 0:
            raise Exception("termux-open-url failed")
    except Exception:
        try:
            webbrowser.open(url)
        except Exception:
            pass


def get_tw():
    """Get terminal width dynamically."""
    try:
        return max(40, os.get_terminal_size().columns - 2)
    except Exception:
        return 50
