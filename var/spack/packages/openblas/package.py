from spack import *
import os

class Openblas(Package):
    """OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."""
    homepage = "http://www.openblas.net/"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')
    version('0.2.14', '53cda7f420e1ba0ea55de536b24c9701')

    version('master', git="https://github.com/xianyi/OpenBLAS.git", branch = 'develop')

    variant('threads', default=False, description='Enable threads')
    variant('shared', default=False, description='Enable shared library')

    provides('blas')
    provides('cblas')
    provides('lapack')

    def setup_dependent_environment(self, module, spec, dep_spec):
        """Dependencies of this package will get the library name for openblas."""
        if spec.satisfies('+shared'):
            module.blaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
            module.blaslibfortname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
            module.cblaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
            module.cblaslibfortname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
            module.lapacklibname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
            module.lapacklibfortname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
        else:
            module.blaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.blaslibfortname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.cblaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.cblaslibfortname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.lapacklibname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.lapacklibfortname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]

    def install(self, spec, prefix):
        make_args = [
            "BINARY=64",
            "DYNAMIC_ARCH=1"
        ]

        if spec.satisfies('+threads'):
            make_args.append("USE_THREAD=1")
        else:
            make_args.append("USE_THREAD=0")

        if spec.satisfies('+shared'):
            make_args.append("NO_STATIC=1")
        else:
            make_args.append("NO_SHARED=1")

        if spec.satisfies('%gcc'):
            make_args.append("FC=gfortran")

        if spec.satisfies('%mkl'):
            make_args.append("FC=ifort")

        make(*make_args)

        # make install needs the other parameters as well
        make_args.append("PREFIX="+prefix+ " install")

        make(*make_args,parallel=False)
        make(*make_args,parallel=False)
