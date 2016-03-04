from spack import *
import re

class DtkTraces(Package):
    """ to use TRACES as a dtk application. """
    homepage = "https://is-dev.inria.fr/tcabel/dtk-traces"

    gitroot = "git@is-dev.inria.fr:tcabel/dtk-traces.git"
    version('master', git=gitroot, branch = 'master')

    variant('dtkio', default=False, description='Enable DTK-IO')

    depends_on("dtk-io", when='+dtkio')
    depends_on("tracesinria")
    depends_on("scotch")
    depends_on("dtk")
    depends_on("dtk-linear-algebra-sparse")
    depends_on("dtk-discrete-geometry@dev")
    depends_on("dtk-plugins-distributed")
    depends_on("dtk-plugins-linear-algebra-sparse+hypre")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):

            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DdtkLinearAlgebraSparse_DIR:PATH=%s" % spec['dtk-linear-algebra-sparse'].prefix+"/cmake/dtkLinearAlgebraSparse",
                "-DdtkDiscreteGeometry_DIR:PATH=%s" % spec['dtk-discrete-geometry'].prefix+"/cmake/dtkDiscreteGeometry",
                "-Dscotch_DIR:PATH=%s" % spec['scotch'].prefix
            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+dtkio'):
                cmake_args.append("-Ddtk_Io_DIR:PATH=%s" % spec['dtk-io'].prefix.lib+"/cmake/dtkIo")

            cmake(*cmake_args)
            make()
            make("install",parallel=False)
