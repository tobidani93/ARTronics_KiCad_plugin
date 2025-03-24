import wx

class PcbToGlbView(wx.Dialog):  # vagy wx.Frame, ha nem modálisan akarod
    def __init__(self, parent, pcb_doc):
        super().__init__(parent, title="Export 3D Model", size=(400, 200))
        self.pcb_doc = pcb_doc

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Cím szöveg középen
        title = wx.StaticText(self, label="Export PCB to 3D (glb) object")
        font = title.GetFont()
        font.PointSize += 2
        font = font.Bold()
        title.SetFont(font)

        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Ide jöhetnek további mezők, beállítások, gombok stb.
        self.SetSizer(vbox)
        self.CentreOnParent()
