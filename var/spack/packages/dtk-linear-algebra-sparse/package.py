from spack import *

class DtkLinearAlgebraSparse(Package):
    """dtk linear algebra sparse is a thematic layer of DTK. """
    homepage = "http://dtk.inria.fr/"

    gitroot = "https://github.com/d-tk/dtk-linear-algebra-sparse.git"
    version('master', git=gitroot, branch = 'master')

    variant('test', default=False, description='Enable test building')

    depends_on("dtk")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk"
            ]
            cmake_args.extend(std_cmake_args)

            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
