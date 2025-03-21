import pcbnew
import wx
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QTextEdit
import os

class ARTronics_plugin(pcbnew.ActionPlugin):
    def defaults(self):
        """Set plugin properties"""
        self.name = "ARTronics"
        self.category = "Example Plugins"
        self.description = "Counts the number of tracks on the PCB"
        self.show_toolbar_button = True
        self.icon_file_name = "../icon.png"

    def Run(self):
        """Executed when the plugin is triggered"""
        board = pcbnew.GetBoard()
        num_tracks = len(board.GetTracks())
        wx.MessageBox(f"The PCB has {num_tracks} tracks!", "ARTronics_plugin")

        """Executed when the plugin is triggered"""
        app = QApplication(sys.argv)
        self.window = KiCadProjectViewer()
        self.window.show()
        app.exec()


class KiCadProjectViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ARTronics KiCad Project Viewer")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Text Fields
        self.text1 = QLineEdit(self)
        self.text1.setPlaceholderText("Enter project name")
        layout.addWidget(self.text1)

        self.text2 = QLineEdit(self)
        self.text2.setPlaceholderText("Enter author name")
        layout.addWidget(self.text2)

        self.text3 = QLineEdit(self)
        self.text3.setPlaceholderText("Enter version")
        layout.addWidget(self.text3)

        # Browse Button
        self.browse_btn = QPushButton("Select Project Folder", self)
        self.browse_btn.clicked.connect(self.load_project_files)
        layout.addWidget(self.browse_btn)

        # File Display
        self.file_display = QTextEdit(self)
        self.file_display.setReadOnly(True)
        layout.addWidget(self.file_display)

        self.setLayout(layout)

    def load_project_files(self):
        """ Select a folder and list KiCad project files """
        folder = QFileDialog.getExistingDirectory(self, "Select KiCad Project Folder")

        if folder:
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

            self.file_display.setText(file_text)