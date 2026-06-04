import os
import socket
import threading
import http.server
import functools
from utils import C

# ============================================
# LOCAL WEB SERVER
# ============================================

DEFAULT_PORT = 8080
DEFAULT_DIR  = "/sdcard"

# Global server instance for stop support
_server_instance = None
_server_thread   = None


def get_local_ip():
    """Get LAN IP address of the device."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr(url):
    """Generate QR code in terminal. Falls back silently if not installed."""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        print(f"\n{C.CYAN}  QR Code (LAN):{C.RESET}")
        qr.print_ascii(invert=True)
    except ImportError:
        pass


def is_server_running():
    return _server_instance is not None


def stop_server():
    global _server_instance, _server_thread
    if _server_instance:
        _server_instance.shutdown()
        _server_instance = None
        _server_thread   = None
        print(f"\n{C.YELLOW}[!]{C.RESET} Server stopped.\n")
    else:
        print(f"\n{C.YELLOW}[!]{C.RESET} No server is running.\n")
    input(f"{C.DIM}  Press Enter to go back...{C.RESET}")


def start_server():
    global _server_instance, _server_thread

    if is_server_running():
        print(f"\n{C.YELLOW}[!]{C.RESET} A server is already running. Stop it first.\n")
        input(f"{C.DIM}  Press Enter to go back...{C.RESET}")
        return

    print(f"\n{C.CYAN}{'─' * 52}{C.RESET}")
    print(f"{C.YELLOW}{C.BOLD}  Start Local Server{C.RESET}")
    print(f"{C.CYAN}{'─' * 52}{C.RESET}\n")

    # --- Folder path ---
    print(f"{C.WHITE}  Folder path (Enter for /sdcard): {C.RESET}", end="")
    folder = input().strip()
    if not folder:
        folder = DEFAULT_DIR

    if not os.path.isdir(folder):
        print(f"\n{C.RED}[x]{C.RESET} Folder not found: {folder}\n")
        input(f"{C.DIM}  Press Enter to go back...{C.RESET}")
        return

    # --- Port ---
    print(f"{C.WHITE}  Port (Enter for {DEFAULT_PORT}): {C.RESET}", end="")
    port_input = input().strip()
    try:
        port = int(port_input) if port_input else DEFAULT_PORT
        if not (1024 <= port <= 65535):
            raise ValueError
    except ValueError:
        print(f"\n{C.YELLOW}[!]{C.RESET} Invalid port. Using {DEFAULT_PORT}.\n")
        port = DEFAULT_PORT

    # --- Start server in background thread ---
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=folder)

    try:
        httpd = http.server.HTTPServer(("0.0.0.0", port), handler)
    except OSError as e:
        print(f"\n{C.RED}[x]{C.RESET} Could not start server: {e}\n")
        input(f"{C.DIM}  Press Enter to go back...{C.RESET}")
        return

    _server_instance = httpd
    _server_thread   = threading.Thread(target=httpd.serve_forever, daemon=True)
    _server_thread.start()

    local_ip  = get_local_ip()
    local_url = f"http://localhost:{port}"
    lan_url   = f"http://{local_ip}:{port}"

    print(f"\n{C.GREEN}[+]{C.RESET} Server started!\n")
    print(f"  {C.CYAN}Folder   :{C.RESET} {folder}")
    print(f"  {C.CYAN}Local    :{C.RESET} {C.YELLOW}{local_url}{C.RESET}")
    print(f"  {C.CYAN}LAN      :{C.RESET} {C.YELLOW}{lan_url}{C.RESET}")

    generate_qr(lan_url)

    print(f"\n{C.DIM}  Server running in background. Use 'Stop Server' from menu to stop.{C.RESET}\n")
    print(f"{C.CYAN}{'─' * 52}{C.RESET}")

    input(f"\n{C.DIM}  Press Enter to go back to menu...{C.RESET}")
