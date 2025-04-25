from argparse import ArgumentParser
from utils import check_file, print_dictinfo, match_and_get, zip_files
from popen_impl import popen_impl
from pathlib import Path
from compiler.clang import CompilerClang
from compiler.gcc import CompilerGCC
from datetime import datetime
import os
import shutil
from loginit import logging
from typing import Optional

class KernelBuild:
    ADDITIONALARGS_LLVM_FULL = ['LLVM=1', 'LLVM_IAS=1']

    def __init__(self, name: str, arch : str, kernelType: str, anykernelDir: Optional[Path] = None, toolchainDir: Optional[Path] = None, outDir: Optional[Path] = None):
        self.kernel_name = name
        self.toolchainDir = toolchainDir if toolchainDir else Path('toolchain')
        self.outDir = outDir if outDir else Path('out')
        self.anykernelDir = anykernelDir
        self.arch = arch
        self.kernelType = kernelType

    def initArgParser(self):
        self.argparser = ArgumentParser(
            description=f'Build {self.kernel_name} with specified arguments'
        )
        self.argparser.add_argument('--allow-dirty', action='store_true', help='Allow dirty builds')

    def initFiles(self):
        # Check for submodules existence and update it if needed.
        if check_file(Path('.gitmodules')):
            popen_impl(['git', 'submodule', 'update', '--init'])
        
        if not check_file(self.toolchainDir):
            logging.error(f'Please make toolchain available at {self.toolchainDir}')
        
    def selectToolchain(self):
        maybeExe = self.toolchainDir / 'bin' / 'clang'
        if check_file(maybeExe):
            self.toolchaincls = CompilerClang(maybeExe)
            logging.info('Detected clang toolchain')
        else:
            # TODO: Generalize this
            maybeExe = self.toolchainDir / 'bin' / 'aarch64-linux-android-gcc'
            self.toolchaincls = CompilerGCC(maybeExe)
        
        self.toolchaincls.test()
        self.toolchainDir = self.toolchainDir.absolute()
    
    # Meant to be overriden
    def buildDefconfigList(self) -> 'list[str]':
        return []

    # Meant to be overriden
    def additionalArgs(self) -> 'list[str]':
        return []
    
    def zipName(_, name: str, time: str):
        return f'{name}Kernel_{time}.zip'
    
    def anykernelFiles(self) -> 'list[str]':
        return []

    def doBuild(self):
        print_dictinfo({
            'TARGET_KERNEL': self.kernel_name,
            'USING_TOOLCHAIN': self.toolchaincls.version(),
            'START_TIME': str(datetime.now())
        })

        # Add toolchain in PATH environment variable
        tcPath = self.toolchainDir / 'bin'
        if tcPath not in os.environ['PATH'].split(os.pathsep):
            os.environ["PATH"] = f'{tcPath}:{os.environ["PATH"]}'
        
        if self.outDir.exists() and not self.args.allow_dirty:
            logging.debug(f'Removing {self.outDir}')
            shutil.rmtree(self.outDir)
        
        common_make = ['make', f'O={self.outDir}', f'-j{os.cpu_count()}', f'ARCH={self.arch}']
        common_make += self.additionalArgs()
        make_defconfig : 'list[str]' = []
        make_defconfig += common_make
        make_defconfig += self.buildDefconfigList()

        t = datetime.now()
        logging.info('Make defconfig')
        popen_impl(make_defconfig)
        logging.info('Make kernel')
        popen_impl(common_make)
        logging.info('Done')
        t = datetime.now() - t

        kver = ''
        with open(self.outDir / 'include' / 'generated' / 'utsrelease.h') as f:
            kver = match_and_get(r'"([^"]+)"', f.read())
        
        if self.anykernelDir:
            shutil.copyfile(self.outDir / 'arch' / Path(self.arch) / 'boot' / Path(self.kernelType), self.anykernelDir / Path(self.kernelType))
            zipName = self.zipName(self.kernel_name, datetime.today().strftime('%Y-%m-%d'))
            os.chdir(self.anykernelDir)
            defFiles = [
                self.kernelType, 
                'META-INF/com/google/android/update-binary',
                'META-INF/com/google/android/updater-script',
                'tools/ak3-core.sh',
                'tools/busybox',
                'tools/magiskboot',
                'anykernel.sh'
            ]
            defFiles += self.anykernelFiles()
            zip_files(zipName, defFiles)
            os.chdir('..')
            shutil.move(self.anykernelDir / Path(zipName), zipName)
            print_dictinfo({
                'OUT_ZIPNAME': zipName,
                'KERNEL_VERSION': kver,
                'ESCLAPED_TIME': str(t.total_seconds()) + ' seconds'
            })
    
    def build(self):
        self.initArgParser()
        self.args = self.argparser.parse_args()
        self.initFiles()
        self.selectToolchain()
        self.doBuild()
        
