from spack import *
import os
import platform
import spack
import sys
from shutil import copyfile

class Pastix(Package):
    """a high performance parallel solver for very large sparse linear systems based on direct methods"""
    homepage = "http://pastix.gforge.inria.fr/files/README-txt.html"

    version('5.2.2.20', '67a1a054fad0f4c5bcbd7abe855667a8',
            url='https://gforge.inria.fr/frs/download.php/file/34392/pastix_5.2.2.20.tar.bz2')
    version('5.2.2.22', '85127ecdfaeed39e850c996b78573d94',
            url='https://gforge.inria.fr/frs/download.php/file/35070/pastix_5.2.2.22.tar.bz2')
    version('master', git='https://scm.gforge.inria.fr/anonscm/git/ricar/ricar.git', branch='master')
    version('develop', git='https://scm.gforge.inria.fr/anonscm/git/ricar/ricar.git', branch='develop')

    variant('mpi', default=False, description='Enable MPI')
    variant('smp', default=True, description='Enable Thread')
    variant('cuda', default=False, description='Enable CUDA kernels. Caution: only available if StarPU variant is enabled')
    variant('metis', default=False, description='Enable Metis')
    variant('starpu', default=False, description='Enable StarPU')
    variant('shared', default=True, description='Build Pastix as a shared library')
    variant('examples', default=True, description='Enable compilation and installation of example executables')
    variant('debug', default=False, description='Enable debug symbols')
    variant('int64', default=False, description='To use 64 bits integers')

    depends_on("hwloc")
    depends_on("mpi", when='+mpi')
    depends_on("blas")
    depends_on("scotch")
    depends_on("metis@:4", when='+metis')
    depends_on("starpu~mpi", when='+starpu~mpi')
    depends_on("starpu+mpi", when='+starpu+mpi')

    def setup(self):

        copyfile('config/LINUX-GNU.in', 'config.in')

        mf = FileFilter('config.in')
        spec = self.spec

        # it seems we set CXXPROG twice but it is because in some
        # versions the line exists, and we can filter it, and in some
        # versions it does not
        if spec.satisfies('^starpu@1.2:') or spec.satisfies('^starpu@svn-trunk'):
            mf.filter('CCPROG      = gcc', 'CCPROG      = cc -Wall -DSTARPU_1_2\nCXXPROG     = c++')
        else:
            mf.filter('CCPROG      = gcc', 'CCPROG      = cc -Wall \nCXXPROG     = c++')

        mf.filter('CXXPROG     = g\+\+', 'CXXPROG     = c++')
        mf.filter('CFPROG      = gfortran', 'CFPROG      = f77')
        mf.filter('CF90PROG    = gfortran', 'CF90PROG    = fc')

        if spec.satisfies('%xl'):
            mf.filter('CCPROG      = cc -Wall', 'CCPROG      = cc -O2 -fPIC -qsmp -qlanglvl=extended -qarch=auto -qhot -qtune=pwr8')
            mf.filter('CXXPROG     = c\+\+', 'CXXPROG     = c++ -O2 -qsmp -fPIC  -qlanglvl=extended -qarch=auto -qhot -qtune=pwr8')
            mf.filter('CFPROG      = f77', 'CFPROG      = f77 -O2 -fPIC -qsmp -qextname -qhot -qtune=pwr8')
            mf.filter('CF90PROG    = fc', 'CF90PROG    = fc -O2 -qsmp -qextname -fPIC -qlanglvl=extended -qarch=auto -qhot -qtune=pwr8  -qlanglvl=90std')

        mf.filter('^# ROOT          =.*', 'ROOT          = %s' % spec.prefix)
        mf.filter('^# INCLUDEDIR    =.*', 'INCLUDEDIR    = ${ROOT}/include')
        mf.filter('^# LIBDIR        =.*', 'LIBDIR        = ${ROOT}/lib')
        mf.filter('^# BINDIR        =.*', 'BINDIR        = ${ROOT}/bin')
        mf.filter('^# PYTHON_PREFIX =.*', 'PYTHON_PREFIX = ${ROOT}')

        if spec.satisfies('%intel'):
            mf.filter('-lgfortran', '-lifcore')
            mf.filter('^CF90CCPOPT  =.*', 'CF90CCPOPT  = -fpp')

        if spec.satisfies('+shared'):
            mf.filter('#SHARED=1', 'SHARED=1')
            mf.filter('#SOEXT=\.so', 'SOEXT=.so')
            mf.filter('#SHARED_FLAGS =  -shared -Wl,-soname,__SO_NAME__', 'SHARED_FLAGS =  -shared')
            if platform.system() == 'Darwin':
                mf.filter('\.so', '.dylib')
                mf.filter('-shared -Wl,-soname,__SO_NAME__', '-shared')
            mf.filter('#CCFDEB       := \$\{CCFDEB\} -fPIC', 'CCFDEB       := ${CCFDEB} -fPIC')
            mf.filter('#CCFOPT       := \$\{CCFOPT\} -fPIC', 'CCFOPT       := ${CCFOPT} -fPIC')
            mf.filter('#CFPROG       := \$\{CFPROG\} -fPIC', 'CFPROG       := ${CFPROG} -fPIC')

        if spec.satisfies('+int64'):
            mf.filter('#VERSIONINT  = _int64', 'VERSIONINT  = _int64')
            mf.filter('#CCTYPES     = -DINTSSIZE64', 'CCTYPES     = -DINTSSIZE64')
        else:
            mf.filter('#VERSIONINT  = _int32', 'VERSIONINT  = _int32')
            mf.filter('#CCTYPES     = -DINTSIZE32', 'CCTYPES     = -DINTSSIZE32')

        if spec.satisfies('~smp'):
            mf.filter('#VERSIONSMP  = _nosmp', 'VERSIONSMP  = _nosmp')
            mf.filter('#CCTYPES    := \$\(CCTYPES\) -DFORCE_NOSMP', 'CCTYPES    := $(CCTYPES) -DFORCE_NOSMP')

        if spec.satisfies('+mpi'):
            mpi = spec['mpi'].prefix
            try:
                mpicc = binmpicc
            except NameError:
                mpicc = 'mpicc'
            try:
                mpicxx = binmpicxx
            except NameError:
                mpicxx = 'mpic++'
            # it seems we set CXXPROG twice but it is because in some
            # versions the line exists, and we can filter it, and in
            # some versions it does not
            if spec.satisfies('^starpu@1.2:') or spec.satisfies('^starpu@svn-trunk'):
                mf.filter('^MPCCPROG    =.*', 'MPCCPROG    = %s -DSTARPU_1_2\nMPCXXPROG   = %s'%(binmpicc, binmpicxx))
            else:
                mf.filter('^MPCCPROG    =.*', 'MPCCPROG    = %s\nMPCXXPROG   = %s'%(binmpicc, binmpicxx))

            mf.filter('^MPCXXPROG   =.*', 'MPCXXPROG   = %s' % binmpicxx)
            if spec.satisfies('^simgrid'):
                mf.filter('^#CCPASTIX   := \$\(CCPASTIX\) -DPASTIX_FUNNELED', 'CCPASTIX   := $(CCPASTIX) -DPASTIX_SINGLE')
        else:
            mf.filter('^#VERSIONMPI  = _nompi', 'VERSIONMPI  = _nompi')
            mf.filter('^#CCTYPES    := \$\(CCTYPES\) -DFORCE_NOMPI', 'CCTYPES    := $(CCTYPES) -DFORCE_NOMPI')
            mf.filter('MPCCPROG    =.*', 'MPCCPROG    = $(CCPROG)\nMPCXXPROG   = $(CXXPROG)')
            mf.filter('MPCXXPROG   =.*', 'MPCXXPROG   = $(CXXPROG)')
            mf.filter('MCFPROG     =.*', 'MCFPROG     = $(CFPROG)')

        if spec.satisfies('+starpu'):
            starpu = spec['starpu'].prefix
            if '^starpu+mpi' in spec:
                mf.filter('^#CCPASTIX   := \$\(CCPASTIX\) `pkg-config libstarpu --cflags` -DWITH_STARPU', 'CCPASTIX   := $(CCPASTIX) `pkg-config libstarpumpi --cflags` -DWITH_STARPU')
                mf.filter('^#EXTRALIB   := \$\(EXTRALIB\) `pkg-config libstarpu --libs`', 'EXTRALIB   := $(EXTRALIB) `pkg-config libstarpumpi --libs`')
            else:
                mf.filter('^#CCPASTIX   := \$\(CCPASTIX\) `pkg-config libstarpu --cflags` -DWITH_STARPU', 'CCPASTIX   := $(CCPASTIX) `pkg-config libstarpu --cflags` -DWITH_STARPU')
                mf.filter('^#EXTRALIB   := \$\(EXTRALIB\) `pkg-config libstarpu --libs`', 'EXTRALIB   := $(EXTRALIB) `pkg-config libstarpu --libs`')

        if spec.satisfies('+metis'):
            metis = spec['metis'].prefix
            metis_libs = " ".join(metislibname)
            mf.filter('^#VERSIONORD  = _metis', 'VERSIONORD  = _metis')
            mf.filter('^#METIS_HOME  =.*', 'METIS_HOME  = %s' % metis)
            mf.filter('^#CCPASTIX   := \$\(CCPASTIX\) -DMETIS -I\$\(METIS_HOME\)/Lib', 'CCPASTIX   := $(CCPASTIX) -DMETIS -I$(METIS_HOME)/include')
            mf.filter('^#EXTRALIB   := \$\(EXTRALIB\) -L\$\(METIS_HOME\) -lmetis', 'EXTRALIB   := $(EXTRALIB) -L$(METIS_HOME)/lib -lmetis')

        scotch = spec['scotch'].prefix
        scotch_libs = " ".join(scotchlibname)
        mf.filter('^SCOTCH_HOME \?= \$\{HOME\}/scotch_5.1/', 'SCOTCH_HOME = %s' % scotch)
        if not spec.satisfies('^scotch+mpi'):
            mf.filter('#CCPASTIX   := \$\(CCPASTIX\) -I\$\(SCOTCH_INC\) -DWITH_SCOTCH',
                      'CCPASTIX   := $(CCPASTIX) -I$(SCOTCH_INC) -DWITH_SCOTCH')
            mf.filter('#EXTRALIB   := \$\(EXTRALIB\) -L\$\(SCOTCH_LIB\) -lscotch -lscotcherrexit',
                      'EXTRALIB   := $(EXTRALIB) -L$(SCOTCH_LIB) -lscotch -lscotcherrexit -lz -lm -lpthread')
            mf.filter('CCPASTIX   := \$\(CCPASTIX\) -I\$\(SCOTCH_INC\) -DDISTRIBUTED -DWITH_SCOTCH',
                      '#CCPASTIX   := $(CCPASTIX) -I$(SCOTCH_INC) -DDISTRIBUTED -DWITH_SCOTCH')
            mf.filter('EXTRALIB   := \$\(EXTRALIB\) -L\$\(SCOTCH_LIB\) -lptscotch -lscotch -lptscotcherrexit',
                      '#EXTRALIB   := $(EXTRALIB) -L$(SCOTCH_LIB) -lptscotch -lscotch -lptscotcherrexit')
        elif '^scotch@6:' in spec:
            mf.filter('EXTRALIB   := \$\(EXTRALIB\) -L\$\(SCOTCH_LIB\) -lptscotch -lscotch -lptscotcherrexit',
                      'EXTRALIB   := $(EXTRALIB) -L$(SCOTCH_LIB) -lptscotch -lscotch -lptscotcherrexit -lz -lm -lpthread')
        else:
            mf.filter('#EXTRALIB   := \$\(EXTRALIB\) -L\$\(SCOTCH_LIB\) -lptscotch -lptscotcherrexit',
                      'EXTRALIB   := $(EXTRALIB) -L$(SCOTCH_LIB) -lptscotch -lptscotcherrexit -lz -lm -lpthread')
            mf.filter('EXTRALIB   := \$\(EXTRALIB\) -L\$\(SCOTCH_LIB\) -lptscotch -lscotch -lptscotcherrexit',
                      '#EXTRALIB   := $(EXTRALIB) -L$(SCOTCH_LIB) -lptscotch -lscotch -lptscotcherrexit')
        hwloc = spec['hwloc'].prefix
        mf.filter('^HWLOC_HOME \?= /opt/hwloc/', 'HWLOC_HOME = %s' % hwloc)

        blas = spec['blas'].prefix
        blas_libs = " ".join(blaslibname)
        if '^netlib-blas' in spec:
            mf.filter('BLASLIB  = -lblas', 'BLASLIB  = -L%s -lblas -lm' % blas.lib)
        elif '^mkl-blas' in spec:
            mf.filter('BLASLIB  = -lblas', 'BLASLIB  = %s' % blas_libs)
        elif '^openblas' in spec:
            mf.filter('BLASLIB  = -lblas', 'BLASLIB  = -L%s -lopenblas' % blas.lib)
        elif '^eigen-blas' in spec:
            mf.filter('BLASLIB  = -lblas', 'BLASLIB  = -L%s -leigen_blas' % blas.lib)
        elif '^essl-blas' in spec:
            mf.filter('BLASLIB  = -lblas', 'BLASLIB  = %s' % blas_libs)

        mf.filter('LDFLAGS  = $(EXTRALIB) $(BLASLIB)', 'LDFLAGS  = $(BLASLIB) $(EXTRALIB)')

        if platform.system() == 'Darwin':
            mf.filter('-lrt', '')
            mf.filter('i686_pc_linux', 'i686_mac')

    def install(self, spec, prefix):

        with working_dir('src'):

            self.setup()
            if spec.satisfies('+debug'):
                make('debug')
            else:
                make()
            if spec.satisfies('+examples'):
                make('examples')
            make("install")
            # examples are not installed by default
            if spec.satisfies('+examples'):
                install_tree('example/bin', prefix + '/examples')
                install_tree('matrix', prefix + '/matrix')

