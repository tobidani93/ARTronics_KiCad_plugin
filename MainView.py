import wx
import pcbnew
import os
import glob
from functools import partial


from .LocalExportView import LocalExportView
from .CloudExportView import CloudExportView
from .PcbToGlbView import PcbToGlbView
from .Schematic import Schematic
from .PcbDoc import PcbDoc
from .GlbModel import GlbModel

class MainView(wx.Panel):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.schematics_list = []  # List of Schematic objects
        self.schem_checkbox_controls = []
        self.pcb_list = []
        self.pcb_checkbox_controls = []

        self.glb_list = []
        self.glb_checkbox_controls = []

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Cím felül
        title = wx.StaticText(self, label="Android application project exporter")
        title_font = title.GetFont()
        title_font.PointSize += 2
        title_font = title_font.Bold()
        title.SetFont(title_font)

        self.vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        board = pcbnew.GetBoard()
        pcb_file_path = board.GetFileName()
        self.project_dir = os.path.dirname(pcb_file_path)
        self.project_name = os.path.splitext(os.path.basename(pcb_file_path))[0]
        name_label = wx.StaticText(self, label=f"Project name: {self.project_name}")



        self.vbox.Add(name_label, 0, wx.ALL | wx.CENTER, 5)

        # Load Schematics
        self.load_schematics(self.project_dir)

        # Load pcbs
        self.load_pcbs(self.project_dir)

        # Load glbs
        self.load_glbs(self.project_dir)

        # empty spacce
        self.vbox.AddStretchSpacer()




        # Navigation buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.button1 = wx.Button(self, label="Local Export")
        self.button2 = wx.Button(self, label="Export to Cloud")

        hbox.Add(self.button1, 0, wx.ALL, 10)
        hbox.Add(self.button2, 0, wx.ALL, 10)

        self.vbox.Add(hbox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.SetSizer(self.vbox)

        self.button1.Bind(wx.EVT_BUTTON, self.on_button1_click)
        self.button2.Bind(wx.EVT_BUTTON, self.on_button2_click)

    def on_button1_click(self, event):
        selected_schematics = [s for s in self.schematics_list if s.isExporting]
        selected_pcbs = [p for p in self.pcb_list if p.isExporting]
        selected_glbs = [g for g in self.glb_list if g.isExporting]

        # Továbbítjuk az adatokat a LocalExportView-hoz
        self.controller.switch_view(
            LocalExportView,
            project_name = self.project_name,
            schematics=selected_schematics,
            pcbs=selected_pcbs,
            glbs=selected_glbs
        )

    def on_button2_click(self, event):
        self.controller.switch_view(CloudExportView)

    def load_schematics(self, project_dir):
        schematic_paths = glob.glob(os.path.join(project_dir, "**/*.kicad_sch"), recursive=True)
        schematic_paths = [os.path.relpath(p, project_dir) for p in schematic_paths]
        schematic_names = [os.path.basename(p) for p in schematic_paths]

        if not schematic_paths:
            warning = wx.StaticText(self, label="No schematics in project.")
            self.vbox.Add(warning, 0, wx.ALL | wx.LEFT, 10)
            return

        # Cím
        schematic_title = wx.StaticText(self, label="Schematic files:")
        self.vbox.Add(schematic_title, 0, wx.ALL | wx.TOP, 10)

        for name, rel_path in zip(schematic_names, schematic_paths):
            schematic = Schematic(name, rel_path, isExporting=True)
            self.schematics_list.append(schematic)

            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            checkbox = wx.CheckBox(self)
            checkbox.SetValue(True)
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_schem_checkbox_toggle)

            self.schem_checkbox_controls.append((checkbox, schematic))

            label = wx.StaticText(self, label=name)
            row_sizer.Add(checkbox, 0, wx.ALL | wx.CENTER, 5)
            row_sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)
            self.vbox.Add(row_sizer, 0, wx.LEFT, 10)

    def on_schem_checkbox_toggle(self, event):
        checkbox = event.GetEventObject()
        # Megkeressük a hozzá tartozó schematric példányt
        for cb, schem in self.schem_checkbox_controls:
            if cb == checkbox:
                schem.isExporting = cb.GetValue()
                print(f"{schem.schematicName} export: {schem.isExporting}")
                break

    def on_pcb_checkbox_toggle(self, event):
        checkbox = event.GetEventObject()
        for cb, pcb_doc in self.pcb_checkbox_controls:
            if cb == checkbox:
                pcb_doc.isExporting = cb.GetValue()
                print(f"{pcb_doc.pcbDocName} export: {pcb_doc.isExporting}")
                break

    def on_glb_checkbox_toggle(self, event):
        checkbox = event.GetEventObject()
        for cb, glb in self.glb_checkbox_controls:
            if cb == checkbox:
                glb.isExporting = cb.GetValue()
                print(f"{glb.glbName} export: {glb.isExporting}")
                break

    def load_glbs(self, project_dir):
        glb_paths = glob.glob(os.path.join(project_dir, "**/*.glb"), recursive=True)
        glb_paths = [os.path.relpath(p, project_dir) for p in glb_paths]
        glb_names = [os.path.basename(p) for p in glb_paths]

        if not glb_paths:
            warning = wx.StaticText(self, label="Nincs GLB fájl a projektben.")
            self.vbox.Add(warning, 0, wx.ALL | wx.LEFT, 10)
            return

        title = wx.StaticText(self, label="GLB fájlok:")
        self.vbox.Add(title, 0, wx.ALL | wx.TOP, 10)

        for name, rel_path in zip(glb_names, glb_paths):
            glb_model = GlbModel(name, rel_path, isExporting=True)
            self.glb_list.append(glb_model)

            row_sizer = wx.BoxSizer(wx.HORIZONTAL)

            checkbox = wx.CheckBox(self)
            checkbox.SetValue(True)
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_glb_checkbox_toggle)

            self.glb_checkbox_controls.append((checkbox, glb_model))

            label = wx.StaticText(self, label=name)
            row_sizer.Add(checkbox, 0, wx.ALL | wx.CENTER, 5)
            row_sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)

            self.vbox.Add(row_sizer, 0, wx.LEFT, 10)

    def load_pcbs(self, project_dir):
        pcb_paths = glob.glob(os.path.join(project_dir, "*.kicad_pcb"))
        pcb_paths = [os.path.relpath(p, project_dir) for p in pcb_paths]
        pcb_names = [os.path.basename(p) for p in pcb_paths]

        if not pcb_paths:
            warning = wx.StaticText(self, label="Nincs PCB fájl.")
            self.vbox.Add(warning, 0, wx.ALL | wx.LEFT, 10)
            return

        title = wx.StaticText(self, label="PCB fájlok:")
        self.vbox.Add(title, 0, wx.ALL | wx.TOP, 10)

        for name, rel_path in zip(pcb_names, pcb_paths):
            pcb_doc = PcbDoc(name, rel_path, isExporting=True)
            self.pcb_list.append(pcb_doc)

            row_sizer = wx.BoxSizer(wx.HORIZONTAL)

            checkbox = wx.CheckBox(self)
            checkbox.SetValue(True)
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_pcb_checkbox_toggle)

            self.pcb_checkbox_controls.append((checkbox, pcb_doc))

            label = wx.StaticText(self, label=name)
            export_btn = wx.Button(self, label="Export")
            export_btn.Bind(wx.EVT_BUTTON, partial(self.on_export_single_pcb, pcb_doc=pcb_doc))

            row_sizer.Add(checkbox, 0, wx.ALL | wx.CENTER, 5)
            row_sizer.Add(label, 1, wx.ALL | wx.CENTER, 5)
            row_sizer.Add(export_btn, 0, wx.ALL | wx.CENTER, 5)

            self.vbox.Add(row_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

    # Export to glb the pcb
    def on_export_single_pcb(self, event, pcb_doc):
        #wx.MessageBox(f"Exportálva: {pcb_doc.pcbDocName}", "Export", wx.OK | wx.ICON_INFORMATION)
        dlg = PcbToGlbView(self, pcb_doc, self.project_dir)
        dlg.ShowModal()  # vagy dlg.Show() ha nem modálisan akarod
        dlg.Destroy()
        self.controller.show_main_view()
