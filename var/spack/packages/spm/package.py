from spack import *

class Spm(Package):

    """SPM is a Fortran Library that encapsulates many Sparse Matrices Libraries (Pastix , Cusp , ...). The idea is to make you clear as clear as possible without having a hard dependecy on Petsc, or Pastix for example. SPM is part from the Pigasus project.
SPM was also designed to treate the special case of Matrices that we get using the IsoGeometric Analysis approach. In the future, it will contain fast solvers and Proconditioners."""


    homepage = "http://ratnani.org/jorek_doc/index.html"

    gitroot = "git+ssh://scm.gforge.inria.fr/gitroot/spmmanager/spmmanager.git"
    version('build-tree', git=gitroot, branch = 'build-tree')

    depends_on("petsc@3.5.4")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):

            print "PETSC_DIR=%s" % spec['petsc'].prefix
            print "MPI_DIR=%s" % spec['mpi'].prefix
            print "BLAS_DIR=%s" % spec['blas'].prefix
            print "LAPACK_DIR=%s" % spec['lapack'].prefix

            cmake_args = [".."]
            cmake_args.extend(std_cmake_args)

            cmake_args.extend(['-DBLAS_DIR=%s' % spec['blas'].prefix.lib])
            cmake_args.extend(['-DLAPACK_DIR=%s' % spec['lapack'].prefix.lib])
            cmake_args.extend(['-DPETSC_DIR=%s' % spec['petsc'].prefix])
            cmake_args.extend(['-DMPI_Fortran_COMPILER=%s/mpif90' % spec['mpi'].prefix.bin])
            cmake_args.extend(['-DMPI_CXX_COMPILER=%s/mpicxx' % spec['mpi'].prefix.bin])
            cmake_args.extend(['-DMPI_C_COMPILER=%s/mpicc' % spec['mpi'].prefix.bin])
            #cmake_args.extend(['-DMPIEXEC=%s/mpiexec' % spec['mpi'].prefix.bin])
            #cmake_args.extend(['-DCMAKE_Fortran_COMPILER=/usr/local/bin/gfortran'])
            cmake_args.extend(['-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix])
            cmake_args.extend(['-DSPM_DEBUG_TRAC:BOOLE=OFF'])
            cmake_args.extend(['-DSPM_SAVE_MATRIX:BOOL=OFF'])

            cmake(*cmake_args)

            make()
            make('test')
            make('install')
