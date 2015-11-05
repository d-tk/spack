from spack import *

class DtkPluginsDistributed(Package):
    """dtk distributed plugins of DTK. """
    homepage = "http://dtk.inria.fr/glop"

    gitroot = "https://github.com/d-tk/dtk-plugins-distributed.git"
    version('master', git=gitroot, branch = 'master')

    variant('test', default=False, description='Enable test building')

    depends_on("dtk")
    depends_on("mpi@:3.0")

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
