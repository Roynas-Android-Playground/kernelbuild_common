from pathlib import Path
from compiler.base import CompilerBase

class CompilerGCC(CompilerBase):
    def __init__(self, exePath: Path):
        self.exe_path = exePath 
        self.versionRe = r"(.*?gcc \(.*\) \d+(\.\d+)*)"