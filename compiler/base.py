from popen_impl import popen_impl
from pathlib import Path
from utils import match_and_get
import subprocess
import logging
from loginit import logging

class CompilerBase:
    def __init__(self, exePath: Path, versionRe: str):
        self.exe_path = exePath
        self.versionRe = versionRe

    def test(self):
        try:
            popen_impl([self.exe_path.as_posix(), '-v'])
        except RuntimeError as e:
            logging.error("Failed to execute compiler, something went wrong")
            raise e

    def version(self):
        s = subprocess.Popen([self.exe_path.as_posix(), '-v'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        _, tcversion = s.communicate()
        tcversion = tcversion.decode('utf-8')
        return match_and_get(self.versionRe, tcversion)