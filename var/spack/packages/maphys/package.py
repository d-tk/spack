from spack import *
import os
import subprocess
import platform
import sys

class Maphys(Package):
    """a Massively Parallel Hybrid Solver."""
    homepage = "https://project.inria.fr/maphys/"
    url      = "http://maphys.gforge.inria.fr/maphys_0.9.3.tar.gz"

    version('0.9.3', 'f52ff32079991163c8905307ce8b8a79',
            url='http://maphys.gforge.inria.fr/maphys_0.9.3.tar.gz')

    svnroot  = "https://scm.gforge.inria.fr/anonscm/svn/maphys/"
    version('svn-maphys-dev',
            svn=svnroot+"branches/maphys-dev")

    variant('mumps', default=False, description='Enable MUMPS direct solver')
    variant('pastix', default=True, description='Enable PASTIX direct solver')
    variant('examples', default=False, description='Enable compilation and installation of example executables')

    depends_on("mpi")
    depends_on("hwloc")
    depends_on("scotch")
    depends_on("blas")
    depends_on("lapack")
    depends_on("pastix", when='+pastix')
    depends_on("mumps", when='+mumps')
    depends_on("scalapack", when='+mumps')

    def setup(self):
        spec = self.spec

        force_symlink('Makefile.inc.example', 'Makefile.inc')
        mf = FileFilter('Makefile.inc')

        mf.filter('prefix := /usr/local', 'prefix := %s' % spec.prefix)

        mpi = spec['mpi'].prefix
        mf.filter('MPIFC := mpif90', 'MPIFC := mpif90 -I%s -fPIC -ffree-form -ffree-line-length-0' % mpi.include)
        mf.filter('MPICC := mpicc', 'MPICC := mpicc -fPIC -I%s' % mpi.include)
        mf.filter('MPIF77 := mpif77', 'MPIF77 := mpif77 -fPIC -I%s' % mpi.include)

        if '^mkl-blas' in spec:
            mf.filter('# THREAD_FCFLAGS \+= -DMULTITHREAD_VERSION -openmp',
                      'THREAD_FCFLAGS += -DMULTITHREAD_VERSION -fopenmp')
            mf.filter('# THREAD_LDFLAGS := -openmp', 'THREAD_LDFLAGS := -fopenmp')

        blas_libs = " ".join(blaslibname)
        try:
            tmg_libs = " ".join(tmglibname)
        except NameError:
            tmg_libs = ''
        lapack_libs=tmg_libs+' '+" ".join(lapacklibname)
        try:
            scalapack_libs = " ".join(scalapacklibname)
        except NameError:
            scalapack_libs = ''
        try:
            blacs_libs = " ".join(blacslibname)
        except NameError:
            blacs_libs = ''
        try:
            scotch_libs = " ".join(scotchlibname)
        except NameError:
            scotch_libs = ''
        try:
            metis_libs = " ".join(metislibname)
        except NameError:
            metis_libs = ''

        if spec.satisfies('+mumps'):
            mumps = mumpsprefix
            mumps_libs = " ".join(mumpslibname)
            mf.filter('^MUMPS_prefix  :=.*', 'MUMPS_prefix  := %s' % mumps)
            mf.filter('^MUMPS_LIBS :=.*', 'MUMPS_LIBS := '+mumps_libs+' '+scalapack_libs+' '+blacs_libs+' '+lapack_libs+' '+blas_libs+' '+scotch_libs+' '+metis_libs)
        else:
            mf.filter('^MUMPS_prefix  :=.*', '#MUMPS_prefix  := version without mumps')
            mf.filter('^MUMPS_LIBS :=.*', 'MUMPS_LIBS  :=')
            mf.filter('^MUMPS_FCFLAGS  :=.*', 'MUMPS_FCFLAGS  := ')
            mf.filter('^MUMPS_FCFLAGS \+=  -I\$\{MUMPS_prefix\}/include', '#MUMPS_FCFLAGS += -I${MUMPS_prefix}/include')
            mf.filter('^MUMPS_FCFLAGS \+= -DLIBMUMPS_USE_LIBSCOTCH', '#MUMPS_FCFLAGS += -DLIBMUMPS_USE_LIBSCOTCH')

        if spec.satisfies('+pastix'):
            pastix = spec['pastix'].prefix
            mf.filter('PASTIX_topdir := \$\(3rdpartyPREFIX\)/pastix/32bits', 'PASTIX_topdir := %s' % pastix)
            pastix_libs=subprocess.check_output([pastix+"/bin/pastix-conf", "--libs"])
            mf.filter('PASTIX_FCFLAGS := -DHAVE_LIBPASTIX -I\$\{PASTIX_topdir\}/install', 'PASTIX_FCFLAGS := -DHAVE_LIBPASTIX -I${PASTIX_topdir}/include')
            mf.filter('PASTIX_LIBS := -L\$\{PASTIX_topdir\}/install -lpastix -lrt', 'PASTIX_LIBS := %s ' % pastix_libs)
        else:
            mf.filter('PASTIX_topdir := \$\(3rdpartyPREFIX\)/pastix/32bits', '#PASTIX_topdir := %s')
            mf.filter('PASTIX_FCFLAGS := -DHAVE_LIBPASTIX -I\$\{PASTIX_topdir\}/install', '#PASTIX_FCFLAGS := -DHAVE_LIBPASTIX -I${PASTIX_topdir}/include')
            mf.filter('PASTIX_LIBS := -L\$\{PASTIX_topdir\}/install -lpastix -lrt', '#PASTIX_LIBS :=')

        if spec.satisfies('~mumps') and spec.satisfies('~pastix'):
            sys.exit('Maphys depends at least on one direct solver, please enable +mumps or +pastix.')

        mf.filter('METIS_topdir  := \$\(3rdpartyPREFIX\)/metis/32bits', '#METIS_topdir  := version without metis')
        mf.filter('METIS_CFLAGS := -DHAVE_LIBMETIS -I\$\{METIS_topdir\}/Lib', 'METIS_CFLAGS := ')
        mf.filter('METIS_FCFLAGS := -DHAVE_LIBMETIS -I\$\{METIS_topdir\}/Lib', 'METIS_FCFLAGS := ')
        mf.filter('METIS_LIBS := -L\$\{METIS_topdir\} -lmetis', 'METIS_LIBS := ')

        scotch = spec['scotch'].prefix
        mf.filter('SCOTCH_prefix := \$\(3rdpartyPREFIX\)/scotch_esmumps/32bits', 'SCOTCH_prefix  := %s' % scotch)
        mf.filter('SCOTCH_LIBS := -L\$\(SCOTCH_prefix\)/lib -lscotch -lscotcherrexit', 'SCOTCH_LIBS := %s' % scotch_libs)

        blas = spec['blas'].prefix
        lapack = spec['lapack'].prefix
        if '^mkl-blas' in spec:
            mf.filter('^LMKLPATH   :=.*', 'LMKLPATH   := %s' % blas.lib)

        mf.filter('^DALGEBRA_PARALLEL_LIBS  :=.*', 'DALGEBRA_PARALLEL_LIBS  := '+scalapack_libs+' '+blacs_libs+' '+lapack_libs+' '+blas_libs)
        mf.filter('^DALGEBRA_SEQUENTIAL_LIBS :=.*', 'DALGEBRA_SEQUENTIAL_LIBS  := '+lapack_libs+' '+blas_libs)

        if '^mkl-blas' in spec or '^mkl-lapack' in spec or '^mkl-scalapack' in spec:
            mf.filter('COMPIL_CFLAGS := -DAdd_', 'COMPIL_CFLAGS := -DAdd_ -m64 -I${MKLROOT}/include')
            mf.filter('FFLAGS := -g -O0', 'FFLAGS := -g -O0 -m64 -I${MKLROOT}/include')
            mf.filter('FCFLAGS := -g -O0', 'FCFLAGS := -g -O0 -DALLOW_NON_INIT -m64 -I${MKLROOT}/include')

        hwloc = spec['hwloc'].prefix
        mf.filter('HWLOC_prefix := /usr/share', 'HWLOC_prefix := %s' % hwloc)

        mf.filter('ALL_FCFLAGS  :=  \$\(FCFLAGS\) -I\$\(abstopsrcdir\)/include -I. \$\(ALGO_FCFLAGS\) \$\(CHECK_FLAGS\)', 'ALL_FCFLAGS  :=  $(FCFLAGS) -I$(abstopsrcdir)/include -I. $(ALGO_FCFLAGS) $(CHECK_FLAGS) $(THREAD_FCFLAGS)')
        mf.filter('THREAD_FCLAGS', 'THREAD_LDFLAGS')

        if platform.system() == 'Darwin':
            mf.filter('-lrt', '');

    def install(self, spec, prefix):

        self.setup()
        make()
        if spec.satisfies('+examples'):
            make('examples')
        make("install", parallel=False)
        install("include/smph_maphys_type_c.h", '%s/include' % prefix)
        install("include/dmph_maphys_type_c.h", '%s/include' % prefix)
        install("include/cmph_maphys_type_c.h", '%s/include' % prefix)
        install("include/zmph_maphys_type_c.h", '%s/include' % prefix)

        if spec.satisfies('+examples'):
            # examples are not installed by default
            install_tree('examples', '%s/lib/maphys/examples' % prefix)
