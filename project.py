import pcbnew
import wx
import os

from .KicadPluginView import KiCadPluginView




class ARTronics_plugin(pcbnew.ActionPlugin):
    def defaults(self):
        """Set plugin properties"""
        self.name = "ARTronics"
        self.category = "Example Plugins"
        self.description = "Counts the number of tracks on the PCB"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "android_icon.png")

    def Run(self):
        """Executed when the plugin is triggered"""
        board = pcbnew.GetBoard()
        num_tracks = len(board.GetTracks())
        #wx.MessageBox(f"The PCB has {num_tracks} tracks!", "ARTronics_plugin")


        self.window = KiCadPluginView()


"""
class Schematic:
    def __init__(self, name, path, isExporting=True):
        self.schematicName = name
        self.schematicPath = path
        self.isExporting = isExporting

class PcbDoc:
    def __init__(self, name, path, isExporting=True):
        self.pcbDocName = name
        self.pcbDocPath = path
        self.isExporting = isExporting
"""

"""
        self.main_panel = wx.Panel(self)  # ez marad mindig, csak a tartalma cserélődik
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(self.vbox)

        self.apiServer = None

        self.apiServer = None
        self.schematics_list = []  # List of Schematic objects
        self.schem_checkbox_controls = []  # (checkbox, schematric) tuplek

        self.pcb_list = []
        self.pcb_checkbox_controls = []

        panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)  # fő sizer elérhető legyen más metódusokból is

        board = pcbnew.GetBoard()
        pcb_file_path = board.GetFileName()
        project_dir = os.path.dirname(pcb_file_path)
        project_name = os.path.splitext(os.path.basename(pcb_file_path))[0]
        self.build_main_gui(project_dir, project_name)  # a jelenlegi GUI-t betöltjük

        # Projekt név
        #name_label = wx.StaticText(panel, label=f"Project name: {project_name}")
        #name_text = wx.TextCtrl(panel)
        #self.vbox.Add(name_label, 0, wx.ALL | wx.CENTER, 5)
        #self.vbox.Add(name_text, 0, wx.ALL | wx.EXPAND, 5)

        # Schematic fájlok betöltése és megjelenítése
        #self.load_schematics(panel, project_dir)
        """
"""
        self.load_pcbs(panel, project_dir)

        # Gombok egymás mellett
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        export_local_btn = wx.Button(panel, label="Export on local network")
        export_cloud_btn = wx.Button(panel, label="Export on Cloud")

        #export_local_btn.Bind(wx.EVT_BUTTON, self.on_export_local)
        #export_cloud_btn.Bind(wx.EVT_BUTTON, self.on_export_cloud)

        button_sizer.Add(export_local_btn, 0, wx.ALL, 10)
        button_sizer.Add(export_cloud_btn, 0, wx.ALL, 10)

        self.vbox.Add(button_sizer, 0, wx.ALIGN_CENTER)

        panel.SetSizer(self.vbox)
        self.Show()
        #textProjectName = wx.StaticText(panel, label=project_name)

        #vbox.Add(textProjectName, 0, wx.EXPAND, 0)

        # Text Fields
        #self.text1 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        #self.text1.SetHint("Enter project name")
        #self.vbox.Add(self.text1, flag=wx.EXPAND | wx.ALL, border=5)

        #self.text2 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        #self.text2.SetHint("Enter author name")
        #self.vbox.Add(self.text2, flag=wx.EXPAND | wx.ALL, border=5)

        #self.text3 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        #self.text3.SetHint("Enter version")
        #self.vbox.Add(self.text3, flag=wx.EXPAND | wx.ALL, border=5)

        # Browse Button
        #self.browse_btn = wx.Button(panel, label="Select Project Folder")
        #self.browse_btn.Bind(wx.EVT_BUTTON, self.load_project_files)
        #self.vbox.Add(self.browse_btn, flag=wx.EXPAND | wx.ALL, border=5)

        # File Display
        #self.file_display = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        #self.vbox.Add(self.file_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # UDP Server Button
        #self.udp_btn = wx.Button(panel, label="Start UDP Server")
        #self.udp_btn.Bind(wx.EVT_BUTTON, self.start_udp_server)
        #self.vbox.Add(self.udp_btn, flag=wx.EXPAND | wx.ALL, border=5)

        #panel.SetSizer(self.vbox)
        #self.Show()

        #self.udpServer = udp_server()
    """

"""
    def on_export_local(self, event):
        self.switch_view(LocalExportView)

    def on_export_cloud(self, event):
        self.switch_view(CloudExportView)

    def show_main_view(self):
        for child in self.main_panel.GetChildren():
            child.Destroy()
        self.vbox.Clear(True)

        board = pcbnew.GetBoard()
        pcb_file_path = board.GetFileName()
        project_dir = os.path.dirname(pcb_file_path)
        project_name = os.path.splitext(os.path.basename(pcb_file_path))[0]

        self.build_main_gui(project_dir, project_name)
        self.main_panel.Layout()

    def switch_view(self, view_class):
        for child in self.main_panel.GetChildren():
            child.Destroy()
        self.vbox.Clear(True)

        # Átadjuk a controllert (saját magát)
        new_view = view_class(self.main_panel, controller=self)
        self.vbox.Add(new_view, 1, wx.EXPAND | wx.ALL, 0)
        self.main_panel.Layout()

    def build_main_gui(self, project_dir, project_name):
        name_label = wx.StaticText(self.main_panel, label=f"Project name: {project_name}")
        name_text = wx.TextCtrl(self.main_panel)

        self.vbox.Add(name_label, 0, wx.ALL | wx.CENTER, 5)
        self.vbox.Add(name_text, 0, wx.ALL | wx.EXPAND, 5)

        self.load_schematics(self.main_panel, project_dir)
        self.load_pcbs(self.main_panel, project_dir)

        # Gombok
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        export_local_btn = wx.Button(self.main_panel, label="Export on local network")
        export_cloud_btn = wx.Button(self.main_panel, label="Export on Cloud")
        export_local_btn.Bind(wx.EVT_BUTTON, self.on_export_local)
        export_cloud_btn.Bind(wx.EVT_BUTTON, self.on_export_cloud)
        button_sizer.Add(export_local_btn, 0, wx.ALL, 10)
        button_sizer.Add(export_cloud_btn, 0, wx.ALL, 10)

        self.vbox.Add(button_sizer, 0, wx.ALIGN_CENTER)



    def load_pcbs(self, panel, project_dir):
        pcb_paths = glob.glob(os.path.join(project_dir, "*.kicad_pcb"))
        pcb_paths = [os.path.relpath(p, project_dir) for p in pcb_paths]
        pcb_names = [os.path.basename(p) for p in pcb_paths]

        if not pcb_paths:
            warning = wx.StaticText(panel, label="Nincs PCB fájl.")
            self.vbox.Add(warning, 0, wx.ALL | wx.LEFT, 10)
            return

        title = wx.StaticText(panel, label="PCB fájlok:")
        self.vbox.Add(title, 0, wx.ALL | wx.TOP, 10)

        for name, rel_path in zip(pcb_names, pcb_paths):
            pcb_doc = PcbDoc(name, rel_path, isExporting=True)
            self.pcb_list.append(pcb_doc)

            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            checkbox = wx.CheckBox(panel)
            checkbox.SetValue(True)
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_pcb_checkbox_toggle)

            self.pcb_checkbox_controls.append((checkbox, pcb_doc))

            label = wx.StaticText(panel, label=name)
            row_sizer.Add(checkbox, 0, wx.ALL | wx.CENTER, 5)
            row_sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)
            self.vbox.Add(row_sizer, 0, wx.LEFT, 10)

    def load_schematics(self, panel, project_dir):
        schematic_paths = glob.glob(os.path.join(project_dir, "**/*.kicad_sch"), recursive=True)
        schematic_paths = [os.path.relpath(p, project_dir) for p in schematic_paths]
        schematic_names = [os.path.basename(p) for p in schematic_paths]

        if not schematic_paths:
            warning = wx.StaticText(panel, label="Nincs schematic fájl a projektben.")
            self.vbox.Add(warning, 0, wx.ALL | wx.LEFT, 10)
            return

        # Cím
        schematic_title = wx.StaticText(panel, label="Schematic fájlok:")
        self.vbox.Add(schematic_title, 0, wx.ALL | wx.TOP, 10)

        for name, rel_path in zip(schematic_names, schematic_paths):
            schematic = Schematic(name, rel_path, isExporting=True)
            self.schematics_list.append(schematic)

            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            checkbox = wx.CheckBox(panel)
            checkbox.SetValue(True)
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_schem_checkbox_toggle)

            self.schem_checkbox_controls.append((checkbox, schematic))

            label = wx.StaticText(panel, label=name)
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
                print(f"{pcb_doc.pcbDocName} exportálás: {pcb_doc.isExporting}")
                break

    def load_project_files(self, event):
       
        dialog = wx.DirDialog(self, "Select KiCad Project Folder", style=wx.DD_DEFAULT_STYLE)

        if dialog.ShowModal() == wx.ID_OK:
            folder = dialog.GetPath()
            files = os.listdir(folder)
            step_file = None
            sch_files = []
            pcb_files = []

            for file in files:
                if file.endswith(".step") or file.endswith(".stp"):
                    step_file = os.path.join(folder, file)
                elif file.endswith(".sch"):
                    sch_files.append(file)
                elif file.endswith(".kicad_pcb"):
                    pcb_files.append(file)

            # Display files
            file_text = f"📂 Project Folder: {folder}\n\n"
            file_text += f"📄 Schematic Files: {', '.join(sch_files) if sch_files else 'None found'}\n"
            file_text += f"📄 PCB Files: {', '.join(pcb_files) if pcb_files else 'None found'}\n"
            file_text += f"🖥 STEP 3D Model: {step_file if step_file else 'None found'}\n"

            #self.file_display.SetValue(file_text)

        dialog.Destroy()
    """
"""
    def start_udp_server(self, event):
        
        self.udpServer.start_udp_server()
        wx.MessageBox("UDP server started!", "Info", wx.OK | wx.ICON_INFORMATION)

    def closeEvent(self, event):
       
        self.udpServer.stop_udp_server()
        event.Skip()  # Continue with normal close operation
    """
"""
     def initApi(self):
        
        self.apiServer = KiCadRestApiServer(
            project_name="",
            schematics=["", ""],
            pcbs=["", ""],
            docs=[]
        )
        self.apiServer.start()
    """


"""
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

        self.socket.close(
        )
    """