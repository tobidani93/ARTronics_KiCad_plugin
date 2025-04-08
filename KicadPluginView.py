import wx
from .MainView import MainView
from .LocalExportView import LocalExportView

class KiCadPluginView(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Android project exporter", size=(800, 800))

        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(self.main_sizer)

        self.show_main_view()
        self.Show()

    def show_main_view(self):
        self.switch_view(MainView)

    def switch_view(self, new_view_class, project_name=None, schematics=None, pcbs=None, glbs=None, images=None):
        # Töröljük a korábbi panelt
        for child in self.main_panel.GetChildren():
            child.Destroy()

        if new_view_class == LocalExportView:
            self.current_view = new_view_class(
                self.main_panel,
                controller=self,
                project_name=project_name,
                schematics=schematics,
                pcbs=pcbs,
                glbs=glbs,
                images=images,
            )
        else:
            self.current_view = new_view_class(
                self.main_panel,
                controller=self
            )

        self.main_sizer.Add(self.current_view, 1, wx.EXPAND)
        self.main_panel.Layout()