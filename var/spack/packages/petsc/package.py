from spack import *

class Petsc(Package):
    """PETSc is a suite of data structures and routines for the
       scalable (parallel) solution of scientific applications modeled by
       partial differential equations."""

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url      = "http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.6.3.tar.gz"

    version('3.6.3', '91dd3522de5a5ef039ff8f50800db606')
    version('3.5.4', '781af0eec1e821f82fb3ecc7a2dfda8e', url="http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.4.tar.gz")
    version('3.5.3', 'd4fd2734661e89f18ac6014b5dd1ef2f', url="http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.3.tar.gz")
    version('3.5.2', 'ad170802b3b058b5deb9cd1f968e7e13', url="http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.2.tar.gz")
    version('3.5.1', 'a557e029711ebf425544e117ffa44d8f', url="http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.5.1.tar.gz")

    variant('openblas', default=True,  description='Enable OpenBlas support for blas and lapack')
    variant('mkl',      default=False, description='Enable MKL support for blas and lapack')
    variant('hypre',    default=False, description='Enable Hypre preconditionners')
    variant('metis',    default=False, description='Enable Metis support')
    variant('parmetis', default=False, description='Enable ParMetis support')
    variant('hdf5',     default=False, description='Enable Hdf5 support')

    depends_on("openblas",   when='~mkl+openblas')
    depends_on("mkl-blas",   when='+mkl')
    depends_on("mkl-lapack", when='+mkl')
    depends_on("blas",       when='~openblas~mkl')
    depends_on("lapack",     when='~openblas~mkl')
    depends_on("mpi")
    depends_on("hypre",      when='+hypre')
    depends_on("metis",      when='+metis')
    depends_on("parmetis",   when='+parmetis')
    depends_on("hdf5",       when='+hdf5')

    def install(self, spec, prefix):
        config_args = ["-prefix=%s" % prefix]

        if spec.satisfies('~openblas') and spec.satisfies('~mkl'):
            config_args.append("--with-blas-lib=%s/libblas.a" % spec['blas'].prefix.lib)
            config_args.append("--with-lapack-lib=%s/liblapack.a" % spec['lapack'].prefix.lib)

        if spec.satisfies('^openblas+shared'):
            config_args.append("--with-blas-lapack-lib=%s/libopenblas.so" % spec['blas'].prefix.lib)

        elif spec.satisfies('+mkl'):
            config_args.append("--with-blas-lapack-dir=%s" % spec['blas'].prefix)

        else:
            config_args.append("--with-blas-lapack-lib=%s/libopenblas.a" % spec['blas'].prefix.lib)

        config_args.append("--with-mpi-dir=%s" % spec['mpi'].prefix)

        if spec.satisfies('+hypre'):
            config_args.append("-with-hypre-dir=%s" % spec['hypre'].prefix)

        if spec.satisfies('+metis'):
            config_args.append("-with-metis-dir=%s" % spec['metis'].prefix)

        if spec.satisfies('+parmetis'):
            config_args.append("-with-parmetis-dir=%s" % spec['parmetis'].prefix)

        if spec.satisfies('+hdf5'):
            config_args.append("-with-hdf5-dir=%s" % spec['hdf5'].prefix)

        print config_args

        configure(*config_args)

        # PETSc has its own way of doing parallel make.
        make('MAKE_NP=%s' % make_jobs, parallel=False)
        make("install")
