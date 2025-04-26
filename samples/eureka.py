from kernelbuild import KernelBuild
from argparse import ArgumentParser
from loginit import logging
from pathlib import Path

class EurekaKernelBuild(KernelBuild):
    def __init__(self):
        super().__init__('Eureka', arch='arm64', kernelType='Image', anykernelDir=Path('AnyKernel3'))
    
    def initArgParser(self) -> ArgumentParser:
        parser = super().initArgParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--oneui', action='store_true', help="OneUI3+ variant")
        group.add_argument('--oneui2', action='store_true', help="OneUI2 variant")
        parser.add_argument('--target', type=str, required=True, help="Target device (a10/a20/...)")
        parser.add_argument('--no-ksu', action='store_true', help="Don't include KernelSU support in kernel")
        return parser

    def verifyArgs(self):
        supplist = ['a10', 'a20', 'a20e', 'a30', 'a30s', 'a40', 'm20', 'jackpotlte']
        if not self.args.target in supplist:
            logging.error(f"Invalid target '{self.args.target}'. Supported: {', '.join(supplist)}")
            return False
        return True
    
    def buildDefconfigList(self) -> 'list[str]':
        args = self.args
        defconfigs = [f'exynos7885-{args.target}_defconfig']
        if args.no_ksu:
            defconfigs.append('noksu.config')
        if args.oneui or args.oneui2:
            defconfigs.append('oneui.config')
        if args.oneui2:
            defconfigs.append('oneui2.config')
        return defconfigs

    def additionalMakeArgs(self) -> 'list[str]':
        return KernelBuild.ADDITIONALARGS_LLVM_FULL + ['CROSS_COMPILE=aarch64-linux-gnu-']

    def preBuildInfo(self) -> 'dict[str, str]':
        args = self.args
        variantStr = 'OneUI' if args.oneui or args.oneui2 else 'AOSP'
        return {
                'TARGET_VARIANT': variantStr,
                'TARGET_DEVICE': args.target,
                'TARGET_INCLUDES_KSU': not args.no_ksu
        }

    def zipName(self, name: str, time: str):
        return f'{name}Kernel_{self.args.target}_{time}.zip'
    
    def anykernelFiles(self) -> 'list[str]':
        return ['version']

def main():
    b = EurekaKernelBuild()
    b.build()

if __name__ == '__main__':
    main()
