from utils import C, print_line, box_line
from config import (
    TOOL_NAME, TOOL_SLOGAN, VERSION,
    AUTHOR, OWNER, GITHUB_URL,
    TELEGRAM_CHANNEL, EMAIL, COPYRIGHT
)

# ============================================
# ASCII BANNER
# ============================================

BANNER = rf"""
{C.CYAN}{C.BOLD}
  ██╗  ██╗ ██████╗ ███████╗████████╗██╗  ██╗
  ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝╚██╗██╔╝
  ███████║██║   ██║███████╗   ██║    ╚███╔╝ 
  ██╔══██║██║   ██║╚════██║   ██║    ██╔██╗ 
  ██║  ██║╚██████╔╝███████║   ██║   ██╔╝ ██╗
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
{C.RESET}"""


def show_banner():
    print(BANNER)
    print(f"{C.CYAN}{'─' * 52}{C.RESET}")
    print(f"{C.YELLOW}{C.BOLD}  {TOOL_SLOGAN}{C.RESET}")
    print(f"{C.CYAN}{'─' * 52}{C.RESET}\n")


def show_info_box():
    w = 50  # inner width (between │ and │)
    border = C.CYAN
    label = C.YELLOW + C.BOLD
    val   = C.WHITE

    def row(lbl, value):
        content = f"{label}{lbl:<12}{C.RESET}{val}{value}"
        box_line(content, width=w, border_color=border, text_color="")

    print(f"{border}╔{'═' * w}╗{C.RESET}")

    # Title row
    title = f"{C.CYAN}{C.BOLD}  {TOOL_NAME}  {C.RESET}{C.DIM}v{VERSION}{C.RESET}"
    box_line(title, width=w, border_color=border, text_color="")

    print(f"{border}╠{'═' * w}╣{C.RESET}")

    row("Version  :", VERSION)
    row("Dev      :", AUTHOR)
    row("Brand    :", OWNER)
    row("GitHub   :", GITHUB_URL)
    row("Channel  :", TELEGRAM_CHANNEL)
    row("Email    :", EMAIL)

    print(f"{border}╠{'═' * w}╣{C.RESET}")

    copy_content = f"{C.DIM}{COPYRIGHT}"
    box_line(copy_content, width=w, border_color=border, text_color="")

    print(f"{border}╚{'═' * w}╝{C.RESET}\n")
