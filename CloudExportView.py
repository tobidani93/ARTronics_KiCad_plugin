import wx

class CloudExportView(wx.Panel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        vbox = wx.BoxSizer(wx.VERTICAL)

        back_btn = wx.Button(self, label="← Vissza")
        back_btn.Bind(wx.EVT_BUTTON, self.on_back)
        vbox.Add(back_btn, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        title = wx.StaticText(self, label="Export to cloud")
        font = title.GetFont()
        font.PointSize += 4
        font = font.Bold()
        title.SetFont(font)
        vbox.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        self.SetSizer(vbox)

    def on_back(self, event):
        self.controller.show_main_view()