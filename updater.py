import re
import sys
import os
import subprocess
import time
import threading
from utils import C, open_url, get_tw
from config import VERSION, GITHUB_REPO, RAW_VERSION_URL, TELEGRAM_CHANNEL, TOOL_NAME

# ============================================
# AUTO UPDATER
# ============================================

def _box(content, width=None, border_color=C.CYAN):
    if width is None: width = get_tw()
    """Print a single box row."""
    import re as _re
    ansi = _re.compile(r'\033\[[0-9;]*m')
    clean = ansi.sub('', content)
    pad = width - len(clean)
    if pad < 0: pad = 0
    print(f"{border_color}│{C.RESET} {content}{' ' * pad}{border_color}│{C.RESET}")


def _box_top(width=None, border_color=C.CYAN):
    if width is None: width = get_tw()
    print(f"{border_color}╔{'═' * width}╗{C.RESET}")

def _box_mid(width=None, border_color=C.CYAN):
    if width is None: width = get_tw()
    print(f"{border_color}╠{'═' * width}╣{C.RESET}")

def _box_bot(width=None, border_color=C.CYAN):
    if width is None: width = get_tw()
    print(f"{border_color}╚{'═' * width}╝{C.RESET}")


def _spinner_check():
    """Show spinner box while checking. Returns (latest_version, elapsed)."""
    frames  = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    result  = [None]
    done    = [False]
    width = get_tw()

    def fetch():
        try:
            import urllib.request
            with urllib.request.urlopen(RAW_VERSION_URL, timeout=6) as resp:
                content = resp.read().decode("utf-8")
            match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                result[0] = match.group(1)
        except Exception:
            pass
        done[0] = True

    t = threading.Thread(target=fetch, daemon=True)
    t.start()

    print()
    _box_top(width)
    i = 0
    while not done[0]:
        frame   = frames[i % len(frames)]
        content = f"{C.CYAN}Checking for updates...{C.RESET}  {C.YELLOW}{frame}{C.RESET}"
        # Overwrite same line inside box
        import re as _re
        ansi = _re.compile(r'\033\[[0-9;]*m')
        clean = _re.sub(r'\033\[[0-9;]*m', '', f"Checking for updates...  {frame}")
        pad   = width - len(clean)
        line  = f"{C.CYAN}│{C.RESET} {C.CYAN}Checking for updates...{C.RESET}  {C.YELLOW}{frame}{C.RESET}{' ' * pad}{C.CYAN}│{C.RESET}"
        print(f"\r{line}", end="", flush=True)
        time.sleep(0.1)
        i += 1

    # Clear spinner line
    print(f"\r{C.CYAN}│{C.RESET} {C.CYAN}Checking for updates...{C.RESET}  {C.GREEN}✓{C.RESET}{' ' * (width - len('Checking for updates...  ✓'))}{C.CYAN}│{C.RESET}")

    t.join()
    return result[0]


def _show_status_box(latest):
    """Show result box after check."""
    width = get_tw()
    _box_mid(width)
    if latest is None:
        _box(f"{C.YELLOW}[!]{C.RESET} Could not reach GitHub", width)
    elif version_tuple(latest) > version_tuple(VERSION):
        _box(f"{C.GREEN}[↑]{C.RESET} New version found!  {C.YELLOW}v{VERSION} → v{latest}{C.RESET}", width)
    else:
        _box(f"{C.GREEN}[✓]{C.RESET} Up to date  {C.DIM}(v{VERSION}){C.RESET}", width)
    _box_bot(width)


def _show_telegram_box():
    """Show Telegram channel box with countdown."""
    width = get_tw()
    print()
    _box_top(width)
    _box(f"{C.YELLOW}Join our Telegram Channel!{C.RESET}", width)
    _box(f"{C.CYAN}{TELEGRAM_CHANNEL}{C.RESET}", width)
    _box_mid(width)

    open_url(TELEGRAM_CHANNEL)

    for i in range(3, 0, -1):
        line = f"{C.DIM}Opening... Going to menu in {C.RESET}{C.YELLOW}{i}s{C.RESET}"
        import re as _re
        clean = _re.sub(r'\033\[[0-9;]*m', '', f"Opening... Going to menu in {i}s")
        pad   = width - len(clean)
        print(f"\r{C.CYAN}│{C.RESET} {line}{' ' * pad}{C.CYAN}│{C.RESET}", end="", flush=True)
        time.sleep(1)

    print(f"\r{C.CYAN}│{C.RESET} {C.DIM}Opening... Going to menu in {C.RESET}{C.GREEN}now!{C.RESET}{' ' * (width - len('Opening... Going to menu in now!'))}{C.CYAN}│{C.RESET}")
    _box_bot(width)
    print()


def version_tuple(v):
    return tuple(int(x) for x in v.strip().split("."))


def check_and_update():
    latest = _spinner_check()
    _show_status_box(latest)

    if latest is not None and version_tuple(latest) > version_tuple(VERSION):
        _show_telegram_box()
        _do_update(latest)
    else:
        _show_telegram_box()


def _do_update(latest):
    """Pull latest files from GitHub using git."""
    width = get_tw()
    tool_dir = os.path.dirname(os.path.abspath(__file__))

    print()
    _box_top(width)
    _box(f"{C.CYAN}Auto-updating {TOOL_NAME}...{C.RESET}", width)
    _box_mid(width)

    if _has_git(tool_dir):
        result = subprocess.run(
            ["git", "pull"],
            cwd=tool_dir,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            _box(f"{C.GREEN}[✓]{C.RESET} Update successful!", width)
            _box(f"{C.YELLOW}[!]{C.RESET} Restarting HostX...", width)
            _box_bot(width)
            time.sleep(2)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            _box(f"{C.RED}[x]{C.RESET} git pull failed. Update manually.", width)
            _box_bot(width)
            input(f"\n{C.DIM}  Press Enter to continue...{C.RESET}")
    else:
        _box(f"{C.YELLOW}[!]{C.RESET} No .git folder. Re-clone from GitHub.", width)
        _box_bot(width)
        input(f"\n{C.DIM}  Press Enter to continue...{C.RESET}")


def _has_git(path):
    return os.path.isdir(os.path.join(path, ".git"))
