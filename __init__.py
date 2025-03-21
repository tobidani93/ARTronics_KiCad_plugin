import pcbnew
from .project import ARTronics_plugin

# Register the plugin so KiCad can load it
ARTronics_plugin().register()