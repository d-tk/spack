from spack import *

class Jorek(Package):
    
    """JOREK-Django is the experimental version for JOREK. The aim of JOREK-Django is to provide

    different meshes: quadrangles, triangles
    different discretizations in the poloidal plan: Hermite Bezier, B-splines, Spectral elements, Box-splines and more generally, a generic Bernstein description
    different discretizations in the toroidal direction: Hermite Bezier, B-splines, Fourier.
    an easy and user-friendly framework to developp and study NonLinear MHD equations
    once compiled as a library, the user can write his own models thanks to a stable interface.
    Linear solvers are provided by the SPM package, which includes (for the moment) PETSC, (PASTIX as well as some other solvers are planned too)
    The code is MPI parallelized."""


    gitroot = "https://iayoub@scm.gforge.inria.fr/authscm/iayoub/git/jorek/jorek.git"
    version('build-new', git=gitroot, branch = 'build-new')
    #jorek-jenkins
    depends_on("spm")
    depends_on("petsc@3.5.4")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")

    
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = [".."]
            cmake_args.extend(std_cmake_args)
            
            
            cmake_args.extend(['-DSPM_INCLUDES=%s' % spec['spm'].prefix.include])
            #cmake_args.extend(['-DSPM_LIBRARIES=%s' % spec['spm'].prefix.lib64])
            cmake_args.extend(['-DSPM_LIBRARY_DIR=%s' % spec['spm'].prefix.lib64])  
            cmake_args.extend(['-DSPM_LIB_SPM=%s/libspm.a' % spec['spm'].prefix.lib64])
            cmake_args.extend(['-DSPM_LIB_TRC=%s/libtracelog.a ' % spec['spm'].prefix.lib64])

            cmake_args.extend(['-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix])

            cmake(*cmake_args)

            make()
            make('test')
            make('install')
