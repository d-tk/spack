from spack import *
import os
import platform

class Openblas(Package):
    """OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."""
    homepage = "http://www.openblas.net/"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')
    version('0.2.14', '53cda7f420e1ba0ea55de536b24c9701')
    version('develop', git='https://github.com/xianyi/OpenBLAS.git', branch='develop')

    variant('mt', default=False, description="Use Multithreaded version")
    variant('openmp', default=False, description="Use Multithreaded version with OpenMP compatibility")
    variant('shared', default=False, description='Enable shared library')
    variant('dynamic', default=True, description='Enable dynamic architecture')

    provides('blas')
    provides('cblas')
    provides('lapack')

    def setup_dependent_environment(self, module, spec, dep_spec):
        """Dependencies of this package will get the library name for openblas."""
        if spec.satisfies('+shared'):
            if platform.system() == 'Darwin':
                module.blaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.dylib")]
                module.cblaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.dylib")]
                module.lapacklibname=[os.path.join(self.spec.prefix.lib, "libopenblas.dylib")]
            else:
                module.blaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
                module.cblaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
                module.lapacklibname=[os.path.join(self.spec.prefix.lib, "libopenblas.so")]
        else:
            module.blaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.cblaslibname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]
            module.lapacklibname=[os.path.join(self.spec.prefix.lib, "libopenblas.a")]

        if spec.satisfies('+mt'):
             module.blaslibname+=["-lpthread"]
        module.blaslibfortname = module.blaslibname
        module.cblaslibfortname = module.cblaslibname
        module.lapacklibfortname = module.lapacklibname


    def install(self, spec, prefix):
        options=['BINARY=64']

        if spec.satisfies('+mt'):
            options.append('USE_THREAD=1')
        else:
            options.append('USE_THREAD=0')

        if spec.satisfies('+openmp'):
            options.append('USE_OPENMP=1')

        if spec.satisfies('+dynamic'):
            options.append('DYNAMIC_ARCH=1')

        if spec.satisfies('+shared'):
            options.append('NO_STATIC=1')
        else:
            options.append('NO_SHARED=1')

        if spec.satisfies('%gcc'):
            options.append('FC=gfortran')

        if spec.satisfies('%mkl'):
            options.append('FC=ifort')

        make(*options)

        # make install needs the other parameters as well (?)
        options.append("PREFIX="+prefix)
        options.append("install")

        make(*options, parallel=False)
