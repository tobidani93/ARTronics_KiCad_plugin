import threading
import socket

class udp_server:
    def __init__(self, http_port):
        self.stop_flag = threading.Event()
        self.server_thread = None
        self.socket = None
        self.HTTP_PORT = http_port

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
        UDP_PORT = 9999
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(("", UDP_PORT))

        while not self.stop_flag.is_set():
            try:
                self.socket.settimeout(1.0)
                data, addr = self.socket.recvfrom(1024)
                server_ip = self.get_local_ip()
                if data.decode() == "DISCOVER_SERVER":
                    response = f"{server_ip}:{self.HTTP_PORT}"
                    self.socket.sendto(response.encode(), addr)
            except socket.timeout:
                continue
            except Exception as e:
                break

        self.socket.close()

    def get_local_ip(self):
        try:
            # Ez próbál egy dummy kapcsolatot, nem küld adatot
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"