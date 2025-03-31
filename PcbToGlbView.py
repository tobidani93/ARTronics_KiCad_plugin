import wx
import os
import platform
import shutil

#/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli

class OptionItem:
    def __init__(self, command, title, checked=False):
        self.command = command
        self.title = title
        self.checked = checked

class PcbToGlbView(wx.Dialog):  # vagy wx.Frame, ha nem modálisan akarod
    def __init__(self, parent, pcb_doc, project_dir):
        super().__init__(parent, title="Export 3D Model", size=(500, 300))
        self.pcb_doc = pcb_doc
        self.project_dir = project_dir

        self.options = [
            OptionItem("--board-only", "Export board only", True),
            OptionItem("--cut-vias-in-body", "Cut vias in board body", False),
            OptionItem("--include-silkscreen", "Export silkscreen", True),
        ]

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)

        self.render_gui()

        self.CentreOnParent()

    def cli_found(self):
        title = wx.StaticText(self, label="Export PCB to 3D (.glb) object")
        font = title.GetFont()
        font.PointSize += 2
        font = font.Bold()
        title.SetFont(font)
        self.vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.vbox.Add(wx.StaticText(self, label=f"CLI: {self.kicad_cli_path}"), 0, wx.ALL, 5)
        self.vbox.Add(wx.StaticText(self, label=f"Project dir: {self.project_dir}"), 0, wx.ALL, 5)

        self.checkboxes = []

        for opt in self.options:
            row = wx.BoxSizer(wx.HORIZONTAL)
            cb = wx.CheckBox(self, label=opt.title)
            cb.SetValue(opt.checked)

            # Eseménykezelő a változtatásra
            cb.Bind(wx.EVT_CHECKBOX, lambda evt, o=opt: self.on_toggle(evt, o))

            row.Add(cb, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
            self.vbox.Add(row, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

            self.checkboxes.append(cb)

        buttons = self.CreateSeparatedButtonSizer(wx.OK | wx.CANCEL)
        if buttons:
            self.vbox.Add(buttons, 0, wx.ALL | wx.EXPAND, 10)

    def on_toggle(self, event, option: OptionItem):
        option.checked = event.IsChecked()

    def cli_not_found(self):
        title = wx.StaticText(self, label="KiCad CLI not found")
        font = title.GetFont()
        font.PointSize += 2
        font = font.Bold()
        title.SetFont(font)
        self.vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

        desc = wx.StaticText(self,
                             label="The KiCad command-line interface (kicad-cli) could not be found.\nPlease check your installation.")
        self.vbox.Add(desc, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 20)

        # Retry gomb: meghívja újra a check függvényt és frissíti a GUI-t
        retry_btn = wx.Button(self, label="Retry")
        retry_btn.Bind(wx.EVT_BUTTON, self.on_retry)
        self.vbox.Add(retry_btn, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        close_btns = self.CreateSeparatedButtonSizer(wx.CLOSE)
        if close_btns:
            self.vbox.Add(close_btns, 0, wx.ALL | wx.EXPAND, 10)

    def render_gui(self):
        # GUI frissítése
        self.vbox.Clear(delete_windows=True)

        self.kicad_cli_path = self.find_kicad_cli()
        if self.kicad_cli_path:
            self.cli_found()
        else:
            self.cli_not_found()

        self.Layout()

    def on_retry(self, event):
        self.render_gui()

    def check_kicad_cli_path(self, path):
        if os.path.isfile(path):
            return True
        else:
            return False


    def find_kicad_cli(self):
        #Check PATH to get cli
        cli_path = shutil.which("kicad-cli")
        if cli_path:
            return cli_path

        #Check by current platform
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

#Exporting with cli:
"""
glb 
[--help] 
[--output OUTPUT_FILE] 
[--define-var KEY=VALUE] 
[--force] Overwrite output file
[--no-unspecified] Exclude 3D models for components with 'Unspecified' footprint type 
[--no-dnp] Exclude 3D models for components with 'Do not populate' attribute 
[--grid-origin] 
[--drill-origin] 
[--subst-models] 
[--board-only] 
[--cut-vias-in-body] 
[--no-board-body] 
[--no-components] 
[--component-filter VAR] 
[--include-tracks] 
[--include-pads] 
[--include-zones] 
[--include-inner-copper] 
[--include-silkscreen] 
[--include-soldermask] 
[--fuse-shapes] 
[--fill-all-vias] 
[--min-distance MIN_DIST] 
[--net-filter VAR] 
[--user-origin VAR] 
INPUT_FILE

test_xil_95108 % /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export glb \
  --output kimenet.glb \
  --subst-models \
  --include-tracks \
  --include-pads \
  --include-zones \
  --include-silkscreen \
  --include-soldermask carte_test.kicad_pcb
"""