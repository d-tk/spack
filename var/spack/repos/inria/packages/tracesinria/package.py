from spack import *
import re

class Tracesinria(Package):
    """ Version INRIA du logiciel TRACES de l'ANDRA dans le cadre de l'IPL C2s_exa """
    homepage = "http://tracesinria.gforge.inria.fr/"

    gitroot = "git+ssh://scm.gforge.inria.fr/gitroot/tracesinria/tracesinria.git"
    version('master', git=gitroot, branch = 'master')
    version('inria', git=gitroot, branch = 'inria')

    variant('dtkio', default=False, description='Enable DTK-IO')
    variant('parallel', default=True, description='Enable parallel code')
    variant('test', default=False, description='Enable test building')

    depends_on("mpi", when='+parallel')
    depends_on("dtk-io", when='+dtkio')
    depends_on("hypre")
    depends_on("dtk")
    depends_on("dtk-linear-algebra-sparse")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):

            cmake_args = [
                "..",
                "-DBUILD_SHARED_LIBS=ON",
                "-DBUILD_DTK=ON",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DdtkLinearAlgebraSparse_DIR:PATH=%s" % spec['dtk-linear-algebra-sparse'].prefix+"/cmake/dtkLinearAlgebraSparse"

            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+dtkio'):
                cmake_args.append("-DBUILD_DTKIO=ON")
                cmake_args.append("-Ddtk_Io_DIR:PATH=%s" % spec['dtk-io'].prefix.lib+"/cmake/dtkIo")

            if spec.satisfies('+mpi'):
                cmake_args.append("-DBUILD_PARALLEL=ON")

            if spec.satisfies('+test'):
                cmake_args.append("-DBUILD_TESTING=ON")

            cmake(*cmake_args)
            make(parallel=False)
            if spec.satisfies('+test'):
               make("test",parallel=False)
            make("install",parallel=False)
