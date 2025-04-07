class ImageFile:
    def __init__(self, name: str, path: str, isExporting=True):
        self.name = name
        self.path = path
        self.isExporting = isExporting