from pathlib import Path
from compiler.base import CompilerBase

class CompilerClang(CompilerBase):
    def __init__(self, exePath: Path):
        self.exe_path = exePath 
        self.versionRe = r"(.*?clang version \d+(\.\d+)*).*"