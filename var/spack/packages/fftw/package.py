from spack import *

class Fftw(Package):
    """a C subroutine library for computing the discrete Fourier transform (DFT) in one or more dimensions, of arbitrary input size, and of both real and complex data."""
    homepage = "http://www.fftw.org/"
    url      = "http://www.fftw.org/fftw-3.3.4.tar.gz"

    version('3.3.4', '2edab8c06b24feeb3b82bbb3ebf3e7b3')

    variant('mpi', default=False, description='Enable MPI')
    variant('openmp', default=False, description='Enable openmp')
    variant('threads', default=False, description='Enable threads')

    depends_on("mpi", when='+mpi')

    def install(self, spec, prefix):

        config_args = ["--prefix=" + prefix]
        config_args.append("--enable-shared")

        if spec.satisfies('+mpi'):
            config_args.append("--enable-mpi")

        if spec.satisfies('+openmp'):
            config_args.append("--enable-openmp")

        if spec.satisfies('+threads'):
            config_args.append("--enable-threads")

        configure(*config_args)
        make()
        make("install")
