from spack import *

class Dtk(Package):
    """dtk is a meta-platform for modular scientific platform development. """
    homepage = "http://dtk.inria.fr/"

    gitroot = "https://github.com/d-tk/dtk.git"
    version('master', git=gitroot, branch = 'master')

    variant('composer', default=False, description='Enable new composer layer')
    variant('wrappers', default=False, description='Enable wrappers')
    variant('test', default=False, description='Enable test building')
    variant('qt', default=False, description='Add explicit dependancy on qt for spack')

    variant('distributedsupport', default=False, description='Enable Distributed support layer')
    variant('coresupport', default=True, description='Enable Core support layer')
    variant('composersupport', default=False, description='Enable Composer support layer')
    variant('vrsupport', default=False, description='Enable VR support layer')
    variant('guisupport', default=False, description='Enable GUI support layer')
    variant('plotsupport', default=False, description='Enable Plot support layer')

    depends_on("qt@5.2.0:", when="+qt")
    depends_on("qwt@6.0.0:", when="+plotsupport")
    depends_on("tcl", when="+wrappers")
    depends_on("swig", when="+wrappers")
    depends_on("mpi", when="+distributedsupport")
    # depends_on("openni", when "+vrsupport")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = [
                ".."
            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+qt'):
                cmake_args.append("-DQT_QMAKE_EXECUTABLE:PATH=%s/qmake" % spec['qt'].prefix.bin)
            else:
                cmake_args.append("-DQT_QMAKE_EXECUTABLE:PATH=qmake-qt5")

            if spec.satisfies('+wrappers'):
                cmake_args.append("-DDTK_BUILD_WRAPPERS")

            if spec.satisfies('+composer'):
                "-DDTK_BUILD_COMPOSER"

            # support layers
            if spec.satisfies('+distributedsupport'):
                "-DDTK_BUILD_SUPPORT_DISTRIBUTED"

            if spec.satisfies('+coresupport'):
                "-DDTK_BUILD_SUPPORT_CORE -DDTK_BUILD_SUPPORT_MATH"

            if spec.satisfies('+composersupport'):
                "-DDTK_BUILD_SUPPORT_COMPOSER"

            if spec.satisfies('+guisupport'):
                "-DDTK_BUILD_SUPPORT_GUI"

            if spec.satisfies('+plotsupport'):
                "-DDTK_BUILD_SUPPORT_PLOT"

            if spec.satisfies('+vrsupport'):
                "-DDTK_BUILD_SUPPORT_PVR"


            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
