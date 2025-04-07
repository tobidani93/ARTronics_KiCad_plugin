import os
import platform
import shutil
import subprocess

"""
 /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb render --output "/Applications/demos/test_xil_95108/carte_test.png" --width 1920 --height 1080 --side top --background default "/Applications/demos/test_xil_95108/carte_test.kicad_pcb"
"""

def render_kicad_png(pcb_path: str, pcb_file_name: str, output_path: str = "") -> bool:
    remove = ".kicad_png"
    pcb_file_name = pcb_file_name.replace(remove, "")
    kicad_cli_path = find_kicad_cli()

    if kicad_cli_path is None:
        print("KiCad CLI not found.")
        return False

    if output_path == "":
        output_path = pcb_path

    output_file = f"{output_path}/{pcb_file_name}.png"
    pcb_file = f"{pcb_path}/{pcb_file_name}.kicad_pcb"

    export_command = [
        kicad_cli_path,
        "pcb", "render",
        "--output", output_file,
        "--width", "1920",
        "--height", "1080",
        "--side", "top",
        "--background", "default",
        pcb_file
    ]

    try:
        subprocess.run(export_command, check=True)
        print(f"Export successful: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Export failed: {e}")
        return False

def find_kicad_cli():
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