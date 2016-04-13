from spack import *
import re

class Num3sisPluginsPrivate(Package):
    """num3sis private plugins. """
    homepage = "http://num3sis.inria.fr/"

    gitroot = "git@dtk.inria.fr:num3sis/num3sis-plugins-private.git"
    version('master', git=gitroot, branch = 'master')

    variant('test', default=False, description='Enable test building')

    depends_on("num3sis")

    def install(self, spec, prefix):


        with working_dir('spack-build', create=True):
            vtk_maj_version  = re.sub('@(\d+\.\d+)\.\d+', '\g<1>',spec['vtk'].format("$@"))
            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DdtkLinearAlgebraSparse_DIR:PATH=%s" % spec['dtk-linear-algebra-sparse'].prefix+"/cmake"
                "-Dnum_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/num3sis",
                "-DVTK_DIR:PATH=%s" % spec['vtk'].prefix.lib+"/cmake/vtk"+vtk_maj_version
            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+qt'):
                cmake_args.append("-DQT_QMAKE_EXECUTABLE:PATH=%s/qmake" % spec['qt'].prefix.bin)
            else:
                cmake_args.append("-DQT_QMAKE_EXECUTABLE:PATH=qmake-qt5")

            if spec.satisfies('+gmsh'):
                gmsh = spec['gmsh'].prefix
                cmake_args.append("-DGMSH_INCLUDE_DIR="+gmsh)
                cmake_args.append("-DGMSH_LIBRARY="+gmsh+"/lib/libGmsh.so")


            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
