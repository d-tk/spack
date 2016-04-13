from spack import *

class DtkPluginsIo(Package):
    """dtk-io plugins of DTK. """
    homepage = "http://dtk.inria.fr/"

    gitroot = "https://github.com/d-tk/dtk-plugins-io.git"
    version('master', git=gitroot, branch = 'master')

    variant('test', default=False, description='Enable test building')
    variant('mpi',  default=False, description='Enable MPI hdf5')

    depends_on("dtk-io")
    depends_on("hdf5")
    # if spec.satisfies('+hdf5'):
    #     depends_on("hdf5+mpi", when"+mpi")
    # else

    def install(self, spec, prefix):


        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DdtkIo_DIR:PATH=%s" % spec['dtk-io'].prefix+"/cmake"
            ]
            cmake_args.extend(std_cmake_args)

            hdf5 = spec['hdf5'].prefix
            cmake_args.append("-DHDF5_IS_PARALLEL=ON" )
            cmake_args.append("-DHDF5_hdf5_LIBRARY_RELEASE=%s" % hdf5.lib )

            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
