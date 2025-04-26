from kernelbuild import KernelBuild

class R3QKernelBuild(KernelBuild):
    def __init__(self):
        super().__init__('Grass', arch='arm64', kernelType='Image', anykernelDir='AnyKernel3')
    
    def initArgParser(self):
        super().initArgParser()
        self.argparser.add_argument('--thin', action='store_true', help="Use ThinLTO for build")

    def buildDefconfigList(self) -> 'list[str]':
        defList = ['r3q_defconfig']
        if self.args.thin:
            defList += ['thinlto.config']
        return defList
    
    def additionalMakeArgs(self) -> 'list[str]':
        return KernelBuild.ADDITIONALARGS_LLVM_FULL

def main():
    b = R3QKernelBuild()
    b.build()

if __name__ == '__main__':
    main()
