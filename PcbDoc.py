class PcbDoc:
    def __init__(self, name, path, isExporting=True):
        self.pcbDocName = name
        self.pcbDocPath = path
        self.isExporting = isExporting