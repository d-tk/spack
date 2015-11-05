from spack import *
import re

class Num3sis(Package):
    """num3sis is a modular platform devoted to scientific computing and numerical simulation. It is not restricted to a particular application field, but is designed to host complex multidisciplinary simulations.. """
    homepage = "http://num3sis.inria.fr/"

    gitroot = "git@dtk.inria.fr:num3sis/num3sis.git"
    version('master', git=gitroot, branch = 'master')
    version('traces', git=gitroot, branch = 'numtraces')
    version('distributed', git=gitroot, branch = 'simulator_new_distributed')

    variant('test', default=False, description='Enable test building')

    variant('aero', default=True, description='Enable aero layer')
    variant('traffic', default=False, description='Enable traffic layer')
    variant('electro', default=False, description='Enable Electro layer')
    variant('design', default=False, description='Enable design layer')
    variant('store', default=False, description='Enable store layer')

    variant('qt', default=True, description='add explicit qt dep')

    #    variant('examples', default=False, description='Enable examples')


    depends_on("dtk+coresupport+composersupport+plotsupport+guisupport+distributedsupport")
    depends_on("dtk-linear-algebra-sparse")
    depends_on("vtk@6.1.0:")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):

            vtk_maj_version  = re.sub('@(\d+\.\d+)\.\d+', '\g<1>',spec['vtk'].format("$@"))

            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DVTK_DIR:PATH=%s" % spec['vtk'].prefix.lib+"/cmake/vtk"+vtk_maj_version
            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+qt'):
                cmake_args.append("-DQT_QMAKE_EXECUTABLE:PATH=%s/qmake" % spec['qt'].prefix.bin)
            else:
                cmake_args.append("-DQT_QMAKE_EXECUTABLE:PATH=qmake-qt5")

            if spec.satisfies('+aero'):
                cmake_args.append("-DBUILD_AERO")
            if spec.satisfies('+design'):
                cmake_args.append("-DBUILD_DESIGN")
            if spec.satisfies('+traffic'):
                cmake_args.append("-DBUILD_TRAFFIC")
            if spec.satisfies('+electro'):
                cmake_args.append("-DBUILD_ELECTRO")
            if spec.satisfies('+store'):
                cmake_args.append("-DBUILD_STORE")

            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
