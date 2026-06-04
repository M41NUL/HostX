import re
import sys
import os
import subprocess
from utils import C, print_line
from config import VERSION, GITHUB_REPO, RAW_VERSION_URL, TELEGRAM_CHANNEL

# ============================================
# AUTO UPDATER
# ============================================

def fetch_latest_version():
    """Fetch latest version string from GitHub raw config.py"""
    try:
        import urllib.request
        with urllib.request.urlopen(RAW_VERSION_URL, timeout=6) as resp:
            content = resp.read().decode("utf-8")
        match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def version_tuple(v):
    return tuple(int(x) for x in v.strip().split("."))


def check_and_update():
    print(f"\n{C.CYAN}[~]{C.RESET} Checking for updates...")

    latest = fetch_latest_version()

    if latest is None:
        print(f"{C.YELLOW}[!]{C.RESET} Could not reach GitHub. Skipping update check.\n")
        return

    if version_tuple(latest) > version_tuple(VERSION):
        print(f"{C.GREEN}[+]{C.RESET} New version found: {C.YELLOW}v{latest}{C.RESET}  (current: v{VERSION})")
        print(f"{C.CYAN}[~]{C.RESET} Auto-updating HostX...\n")
        _do_update()
    else:
        print(f"{C.GREEN}[✓]{C.RESET} HostX is up to date. (v{VERSION})\n")


def _do_update():
    """Pull latest files from GitHub using git or wget fallback."""
    tool_dir = os.path.dirname(os.path.abspath(__file__))

    # Try git pull first
    if _has_git(tool_dir):
        result = subprocess.run(
            ["git", "pull"],
            cwd=tool_dir,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"{C.GREEN}[✓]{C.RESET} Update successful via git!\n")
            print(f"{C.YELLOW}[!]{C.RESET} Restarting HostX...\n")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print(f"{C.RED}[✗]{C.RESET} git pull failed:\n{result.stderr}")
            _manual_update_notice()
    else:
        _manual_update_notice()


def _has_git(path):
    return os.path.isdir(os.path.join(path, ".git"))


def _manual_update_notice():
    print(f"{C.YELLOW}[!]{C.RESET} Auto-update failed. Please update manually:")
    print(f"    {C.CYAN}git pull{C.RESET}  or re-clone from GitHub.\n")
    input(f"{C.DIM}Press Enter to continue with current version...{C.RESET}\n")
