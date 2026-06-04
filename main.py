#!/usr/bin/env python3
"""
HostX - Termux HTML Host Tool
Developer : Md. Mainul Islam (MAINUL-X)
GitHub    : https://github.com/M41NUL
"""

import sys
from utils import clear
from banner import show_banner, show_info_box
from updater import check_and_update
from menu import show_menu, handle_menu

# ============================================
# MAIN ENTRY
# ============================================

def main():
    # 1. Clear screen
    clear()

    # 2. Auto update check
    check_and_update()

    # 3. Main loop
    while True:
        clear()
        show_banner()
        show_info_box()
        show_menu()

        try:
            choice = input().strip()
        except (KeyboardInterrupt, EOFError):
            from menu import do_exit
            do_exit()

        handle_menu(choice)


if __name__ == "__main__":
    main()
