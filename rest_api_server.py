import socket
from werkzeug.serving import make_server
from flask import Flask, send_file, request, jsonify, make_response
import threading
import os

class KiCadRestApiServer:
    def __init__(self, project_name, base_path, schematics, pcbs, models, docs=None):
        self.project_name = project_name
        self.base_path = base_path
        self.schematics = schematics
        self.pcbs = pcbs
        self.models = models
        self.docs = docs if docs else []

        self.port = self._find_free_port(5000, 5100)
        self.ip_address = self._get_local_ip()

        self.app = Flask(__name__)
        self._define_routes()

        self.server_thread = None
        self.http_server = None

    def _find_free_port(self, start, end):
        for port in range(start, end + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if sock.connect_ex(("127.0.0.1", port)) != 0:
                    return port
        raise RuntimeError("No free port available between 5000 and 5100")

    def _get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()

    def _define_routes(self):
        @self.app.route("/project-info", methods=["GET"])
        def get_project_info():
            return jsonify({
                "projectName": self.project_name,
                "schematics": self.schematics,
                "pcbs": self.pcbs,
                "models": self.models
            })

        @self.app.route("/schematic", methods=["GET"])
        def get_schematic():
            return self._send_file_by_name(request.args.get("name"), self.schematics)

        @self.app.route("/pcb", methods=["GET"])
        def get_pcb():
            return self._send_file_by_name(request.args.get("name"), self.pcbs)

        @self.app.route("/model", methods=["GET"])
        def get_model():
            return self._send_file_by_name(request.args.get("name"), self.models)

        @self.app.route("/doc", methods=["GET"])
        def get_doc():
            return self._send_file_by_name(request.args.get("name"), self.docs)

    def _send_file_by_name(self, name, file_list):
        if not name or name not in file_list:
            return make_response(f"File '{name}' not found.", 404)

        file_path = os.path.join(self.base_path, name)

        if not os.path.isfile(file_path):
            return make_response(f"File '{file_path}' does not exist on disk.", 404)

        response = send_file(file_path, as_attachment=True)
        response.headers["Content-Disposition"] = f"attachment; filename={name}"
        return response

    def start(self):
        if self.server_thread and self.server_thread.is_alive():
            return
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()

    def _run_server(self):
        self.http_server = make_server('0.0.0.0', self.port, self.app)
        self.http_server.serve_forever()

    def stop(self):
        if self.http_server:
            self.http_server.shutdown()
            self.server_thread.join()

    def get_url(self):
        return f"http://{self.ip_address}:{self.port}"
