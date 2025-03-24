# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import socket
import threading
import time
from turtledemo.penrose import start
import shutil
import os
import platform


class udp_server:
    def __init__(self):
        self.stop_flag = threading.Event()
        self.server_thread = None
        self.socket = None

    def __del__(self):
        self.stop_udp_server()

    def stop_udp_server(self):
        if self.server_thread and self.server_thread.is_alive():
            self.stop_flag.set()
            self.server_thread.join()

    def start_udp_server(self):
        if self.server_thread and self.server_thread.is_alive():
            return
        self.stop_flag.clear()
        self.server_thread = threading.Thread(target=self._udp_server_thread, daemon=True)
        self.server_thread.start()

    def _udp_server_thread(self):
        """UDP server listening for discovery messages"""
        HTTP_PORT = 5000
        UDP_PORT = 9999
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(("", UDP_PORT))

        while not self.stop_flag.is_set():
            try:
                self.socket.settimeout(1.0)
                data, addr = self.socket.recvfrom(1024)

                if data.decode() == "DISCOVER_SERVER":
                    response = f"{addr[0]}:{HTTP_PORT}"
                    self.socket.sendto(response.encode(), addr)
            except socket.timeout:
                continue
            except Exception as e:
                break

        self.socket.close()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def find_kicad_cli():
    # 1. Próbáljuk meg először a PATH-ból
    cli_path = shutil.which("kicad-cli")
    if cli_path:
        return cli_path

    # 2. Ha nincs a PATH-ban, nézzük meg platform szerint
    system = platform.system()

    if system == "Darwin":  # macOS
        default_path = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
        if os.path.isfile(default_path):
            return default_path

    elif system == "Windows":
        possible_dirs = [
            os.environ.get("ProgramFiles", r"C:\Program Files"),
            os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        ]
        for base in possible_dirs:
            path = os.path.join(base, "KiCad", "bin", "kicad-cli.exe")
            if os.path.isfile(path):
                return path

    elif system == "Linux":
        default_path = "/usr/bin/kicad-cli"
        if os.path.isfile(default_path):
            return default_path

    return None

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cli_path = shutil.which("kicad-cli")
    if cli_path:
        print(f"kicad-cli megtalálva: {cli_path}")
    else:
        print("kicad-cli nem található a PATH-ban.")

    path = find_kicad_cli()
    print(f"{path}")
    #udp_server = udp_server()
    #udp_server.start_udp_server()
    #print("⏳ Várunk 5 másodpercet, hogy a szerver fusson...")
    #time.sleep(50)  # 🔄 Várunk 5 másodpercet, hogy lássuk a szerver működését

    #print("🛑 UDP szerver leállítása teszt módban...")
    #udp_server.stop_udp_server()  # 🔹 Leállítja a szer

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

