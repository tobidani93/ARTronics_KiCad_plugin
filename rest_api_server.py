import socket
import string
from typing import List

from werkzeug.serving import make_server
from flask import Flask, send_file, request, jsonify, make_response
import threading
import os

from .ImageFile import ImageFile
from .GlbModel import GlbModel
from .PcbDoc import PcbDoc
from .Schematic import Schematic
from enum import Enum

class FileType(Enum):
    SCHEMATIC = "schematic"
    PCB = "pcb"
    MODEL = "model"
    DOC = "doc"
    IMAGE = "image"

class KiCadRestApiServer:
    def __init__(self, project_name: string, base_path: string, schematics: List[Schematic], pcbs: List[PcbDoc], models: List[GlbModel], images: List[ImageFile], docs=None):
        self.project_name = project_name
        self.base_path = base_path
        self.schematics = schematics
        self.pcbs = pcbs
        self.models = models
        self.images = images
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
                "schematics": [s.schematicName for s in self.schematics],
                "pcbs": [p.pcbDocName for p in self.pcbs],
                "models": [m.glbName for m in self.models],
                "images": [i.name for i in self.images],
            })

        @self.app.route("/schematic", methods=["GET"])
        def get_schematic():
            return self._send_file_by_name(request.args.get("name"), FileType.SCHEMATIC)

        @self.app.route("/pcb", methods=["GET"])
        def get_pcb():
            return self._send_file_by_name(request.args.get("name"), FileType.PCB)

        @self.app.route("/model", methods=["GET"])
        def get_model():
            return self._send_file_by_name(request.args.get("name"), FileType.MODEL)

        @self.app.route("/doc", methods=["GET"])
        def get_doc():
            return self._send_file_by_name(request.args.get("name"), FileType.DOC)

        @self.app.route("/image", methods=["GET"])
        def get_image():
            return self._send_file_by_name(request.args.get("name"), FileType.IMAGE)

    def _send_file_by_name(self, name,  file_type: FileType):
        #if not name or name not in file_list:
        #    return make_response(f"File '{name}' not found.", 404)
        if not name:
            return make_response("Missing 'name' parameter", 400)

        # Válaszd ki a megfelelő listát és keresendő attribútumot
        if file_type == FileType.SCHEMATIC:
            file_list = self.schematics
            search_attr = "schematicName"
            path_attr = "schematicPath"
        elif file_type == FileType.PCB:
            file_list = self.pcbs
            search_attr = "pcbDocName"
            path_attr = "pcbDocPath"
        elif file_type == FileType.MODEL:
            file_list = self.models
            search_attr = "glbName"
            path_attr = "glbPath"
        elif file_type == FileType.DOC:
            file_list = self.docs
            search_attr = "docName"
            path_attr = "docPath"
        elif file_type == FileType.IMAGE:
            file_list = self.images
            search_attr = "name"
            path_attr = "path"
        else:
            return make_response("Invalid file type", 400)

        # Objektum keresése név alapján
        match = next((obj for obj in file_list if getattr(obj, search_attr, None) == name), None)

        if not match:
            return make_response(f"File '{name}' not found in {file_type.value} list.", 404)


        from pathlib import Path
        file_path = Path(self.base_path) / getattr(match, path_attr)

        if not file_path.is_file():
            return make_response(f"File '{file_path}' does not exist on disk.", 404)

        response = send_file(str(file_path), as_attachment=True)
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

    def get_port(self):
        return self.port

