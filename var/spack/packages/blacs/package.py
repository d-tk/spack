from spack import *
import os
from subprocess import call

class Blacs(Package):
    """The BLACS (Basic Linear Algebra Communication Subprograms) project is an ongoing investigation whose purpose is to create a linear algebra oriented message passing interface that may be implemented efficiently and uniformly across a large range of distributed memory platforms."""

    homepage = "http://www.netlib.org/blacs/"

    # tarball has no version, but on the date below, this MD5 was correct.
    version('1997-05-05', '28ae5b91b3193402fe1ae8d06adcf500', url='http://www.netlib.org/blacs/mpiblacs.tgz')
    version('lib','82687f1e07fd98e0b9f78b71911459fe', url='http://www.netlib.org/blacs/archives/blacs_MPI-LINUX-0.tgz')
    depends_on('mpi')

    variant('shared', default=True, description='Build BLACS as a shared library')

    def install(self, spec, prefix):
        call(['cp', 'BMAKES/Bmake.MPI-LINUX', 'Bmake.inc'])
        mf = FileFilter('Bmake.inc')

        mf.filter('\$\(HOME\)/BLACS', '%s' % os.getcwd())
        mf.filter('/usr/local/mpich', '%s' % self.spec['mpi'].prefix)
        mf.filter('\$\(MPILIBdir\)/libmpich\.a', '')
        mf.filter('\$\(MPIdir\)/lib/', '')
        mf.filter('DUseMpich', 'DUseMpi2')
        mf.filter('F77            = g77', 'F77            = mpif77')
        mf.filter('CC             = gcc', 'CC             = mpicc')

        if spec.satisfies('+shared'):
            mf.filter('ARCH\s*=.*', 'ARCH=$(CC)')
            mf.filter('ARCHFLAGS\s*=.*', 'ARCHFLAGS=-shared -o')
            mf.filter('RANLIB\s*=.*', 'RANLIB=echo')
            mf.filter('CCFLAGS\s*=', 'CCFLAGS = -fPIC ')
            mf.filter('F77FLAGS\s*=', 'F77FLAGS = -fPIC ')
            mf.filter('\.a', '.so')

        filter_file('\$\(MAKE\) -f \.\./Makefile I_int \"dlvl=\$\(BTOPdir\)\" \)','echo $(BLACSDEFS) $(MAKE) -f ../Makefile I_int "dlvl=$(BTOPdir)" )', 'SRC/MPI/Makefile')
        call(['cat', 'Bmake.inc'])
        call(['cat', 'SRC/MPI/Makefile'])

        make('mpi')
        mkdirp(prefix.lib)
        if spec.satisfies('+shared'):
            install('LIB/blacsCinit_MPI-LINUX-0.so', '%s/libblacsCinit.so' % prefix.lib)
            install('LIB/blacsF77init_MPI-LINUX-0.so', '%s/libblacsF77init.so' % prefix.lib)
            install('LIB/blacs_MPI-LINUX-0.so', '%s/libblacs.so' % prefix.lib)
        else:
            install('LIB/blacsCinit_MPI-LINUX-0.a', '%s/libblacsCinit.a' % prefix.lib)
            install('LIB/blacsF77init_MPI-LINUX-0.a', '%s/libblacsF77init.a' % prefix.lib)
            install('LIB/blacs_MPI-LINUX-0.a', '%s/libblacs.a' % prefix.lib)
        	    



