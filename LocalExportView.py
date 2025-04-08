import string
from typing import List

import wx
import pcbnew
import os
from pyassimp.structs import String

from .ImageFile import ImageFile
from .GlbModel import GlbModel
from .PcbDoc import PcbDoc
from .Schematic import Schematic
from .rest_api_server import KiCadRestApiServer
from .UdpServer import udp_server


class LocalExportView(wx.Panel):
    def __init__(self, parent, controller, project_name: string, schematics: List[Schematic], pcbs: List[PcbDoc], glbs: List[GlbModel], images: List[ImageFile]):
        super().__init__(parent)
        self.controller = controller
        self.restServer = None
        self.udpServer = None
        self.project_name = project_name
        self.schematics = schematics
        self.pcbs = pcbs
        self.glbs = glbs
        self.images = images
        self.server_url = ""
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Vissza gomb
        back_btn = wx.Button(self, label="← Vissza")
        back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        vbox.Add(back_btn, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        # Cím
        title = wx.StaticText(self, label="Export on local network")
        font = title.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title.SetFont(font)
        vbox.Add(title, 0, wx.ALIGN_CENTER, 10)
        board = pcbnew.GetBoard()
        self.pcb_file_path = board.GetFileName()
        self.project_dir = os.path.dirname(self.pcb_file_path)

        self.urlLabel = wx.StaticText(self, label=f"Address: {self.server_url}")

        # Betűméret
        font = self.urlLabel.GetFont()
        font.SetPointSize(16)
        self.urlLabel.SetFont(font)

        # Padding
        vbox.Add(self.urlLabel, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        for gl in glbs:
            g = wx.StaticText(self, label=f"{self.project_dir}/{gl.glbName}")
            vbox.Add(g)

        if glbs:
            glb = wx.StaticText(self, label=glbs[0].glbPath)
            vbox.Add(glb)
        else:
            glb = wx.StaticText(self, label="No glb file")
            vbox.Add(glb)

        for im in images:
            im1 = wx.StaticText(self, label=f"{im.name}")
            vbox.Add(im1)

        for pcb in pcbs:
            pcb_text = wx.StaticText(self, label=f"{pcb.pcbDocName}")
            vbox.Add(pcb_text)


        #Start server button
        #hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.exportButton = wx.Button(self, label="Start export")

        vbox.Add(self.exportButton)
        self.exportButton.Bind(wx.EVT_BUTTON, self.start_export)

        #hbox.Add(self.exportButton, 0, wx.ALL, 10)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)



    def on_back(self, event):
        # stop rest server
        if self.restServer:
            self.restServer.stop()
            self.restServer = None
        if self.udpServer:
            self.udpServer.stop_udp_server()
            self.udpServer = None
        self.controller.show_main_view()

    def  start_export(self, event):
        if self.restServer is None:
            self.restServer = KiCadRestApiServer(
                project_name=self.project_name,
                base_path= self.project_dir,
                schematics=self.schematics,
                pcbs=self.pcbs,
                models=self.glbs,
                images=self.images
            )
            self.restServer.start()
            self.server_url = self.restServer.get_url()
            self.urlLabel.SetLabel(f"Address: {self.server_url}")
            port = self.restServer.get_port()
            self.udpServer = udp_server(port)
            self.udpServer.start_udp_server()

    def on_destroy(self, event):
        #stop rest_server when user close the window
        if self.restServer:
            self.restServer.stop()
            self.restServer = None
        if self.udpServer:
            self.udpServer.stop_udp_server()
            self.udpServer = None
        event.Skip()