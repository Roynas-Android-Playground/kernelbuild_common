from kernelbuild import KernelBuild
from argparse import ArgumentParser
from pathlib import Path

class TB128FUKernelBuild(KernelBuild):
    def __init__(self):
        super().__init__('Grass', arch='arm64', kernelType='Image', anykernelDir=Path('AnyKernel3'))
    
    def buildDefconfigList(self) -> 'list[str]':
        return ['grass-perf_defconfig']
    
    def additionalMakeArgs(self) -> 'list[str]':
        return KernelBuild.ADDITIONALARGS_LLVM_FULL

def main():
    b = TB128FUKernelBuild()
    b.build()

if __name__ == '__main__':
    main()
