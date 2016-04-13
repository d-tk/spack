from spack import *
import glob
import os
from subprocess import call
import subprocess
import sys
import spack
import platform
import gzip


def gunzip(file_name):
    inF = gzip.GzipFile(file_name, 'rb')
    s = inF.read()
    inF.close()

    print file_name[:-3]
    outF = file(file_name[:-3], 'wb')
    outF.write(s)
    outF.close()


class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""
    homepage = "http://www.labri.fr/perso/pelegrin/scotch/"
    # url      = "http://gforge.inria.fr/frs/download.php/file/34099/scotch_6.0.3.tar.gz"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.3', '10b0cc0f184de2de99859eafaca83cfc',
            url='http://gforge.inria.fr/frs/download.php/file/34099/scotch_6.0.3.tar.gz')
    version('6.0.4', 'd58b825eb95e1db77efe8c6ff42d329f',
            url='https://gforge.inria.fr/frs/download.php/file/34618/scotch_6.0.4.tar.gz')
    version('5.1.11', 'c00a886895b3895529814303afe0d74e',
            url='https://gforge.inria.fr/frs/download.php/28044/scotch_5.1.11_esmumps.tar.gz')

    variant('mpi', default=False, description='Activate the compilation of PT-Scotch')
    variant('pthread', default=True, description='Enable multithread with pthread')
    variant('compression', default=False, description='Activate the possibility to use compressed files')
    variant('esmumps', default=False, description='Activate the compilation of the lib esmumps needed by mumps')
    variant('shared', default=True, description='Build shared libraries')
    variant('int64', default=False, description='to use 64 bits integers')
    variant('grf', default=False, description='Install grf examples files')

    depends_on('mpi', when='+mpi')
    depends_on('zlib', when='+compression')
    depends_on('flex')
    depends_on('bison')

    def setup_dependent_environment(self, module, spec, dep_spec):
        """Dependencies of this package will get the libraries names for Scotch."""
        if self.spec.satisfies('+shared'):
            libext=".dylib" if platform.system() == 'Darwin' else ".so"
        else:
            libext=".a"
        libdir = self.spec.prefix.lib

        scotchlibname=[os.path.join(libdir, "libscotch%s") % libext]
        scotcherrlibname=[os.path.join(libdir, "libscotcherr%s") % libext]
        scotcherrexitlibname=[os.path.join(libdir, "libscotcherrexit%s") % libext]
        ptscotchlibname=[os.path.join(libdir, "libptscotch%s") % libext]
        ptscotcherrlibname=[os.path.join(libdir, "libptscotcherr%s") % libext]
        ptscotcherrexitlibname=[os.path.join(libdir, "libptscotcherrexit%s") % libext]
        esmumpslibname=[os.path.join(libdir, "libesmumps%s") % libext]
        ptesmumpslibname=[os.path.join(libdir, "libptesmumps%s") % libext]

        otherlibs=["-lm"]
        if self.spec.satisfies('+pthread'):
            otherlibs+=["-lpthread"]
        if self.spec.satisfies('+compression'):
            otherlibs+=["-lz"]
        if platform.system() == 'Linux':
            otherlibs+=["-lrt"]

        module.scotchlibname = []
        if self.spec.satisfies('+esmumps'):
            if self.spec.satisfies('+mpi'):
                module.scotchlibname+=ptesmumpslibname
                module.scotchlibname+=ptscotchlibname
                module.scotchlibname+=ptscotcherrlibname
            module.scotchlibname+=esmumpslibname
        else:
            if self.spec.satisfies('+mpi'):
                module.scotchlibname+=ptscotchlibname
                module.scotchlibname+=ptscotcherrlibname
        module.scotchlibname+=scotchlibname
        module.scotchlibname+=scotcherrlibname
        module.scotchlibname+=otherlibs

    def compiler_specifics(self, makefile_inc, defines):
        if self.spec.satisfies('+mpi'):
            try:
                mpicc = binmpicc
            except NameError:
                mpicc = 'mpicc'
        if self.compiler.name == 'gcc':
            defines.append('-Drestrict=__restrict')
        elif self.compiler.name == 'intel':
            defines.append('-restrict')

        makefile_inc.append('CCS       = $(CC)')

        if self.spec.satisfies('+mpi'):
            makefile_inc.extend([
                    'CCP       = %s' % os.path.join(self.spec['mpi'].prefix.bin, '%s' % mpicc),
                    ])

            if self.spec.satisfies("^simgrid"):
                makefile_inc.extend([
                    'CCD       = cc -I'+self.spec['simgrid'].prefix+'/include/smpi'
                    ])
                filter_file('static MPI_Datatype         dgraphstattypetab\[2\] = \{ GNUM_MPI, MPI_DOUBLE \};', '', 'src/libscotch/library_dgraph_stat.c')
                # Beware: dirty code
                filter_file('velolocdlt = 0.0L;', 'velolocdlt = 0.0L;MPI_Datatype         dgraphstattypetab[2] = { GNUM_MPI, MPI_DOUBLE };', 'src/libscotch/library_dgraph_stat.c')


            else:
                makefile_inc.extend([
                    'CCD       = $(CCP)'
                    ])
        else:
            makefile_inc.extend([
                    'CCP       = mpicc', # It is set but not used
                    'CCD       = $(CCS)'
                    ])

    def library_build_type(self, makefile_inc, defines):
        makefile_inc.extend([
            'LIB       = .a',
            'CLIBFLAGS = ',
            'RANLIB    = ranlib',
            'AR        = ar',
            'ARFLAGS   = -ruv '
            ])

    @when('+shared')
    def library_build_type(self, makefile_inc, defines):
        if platform.system() == 'Darwin':
            libext = ".dylib"
            addarflags = "-undefined dynamic_lookup"
        else:
            libext = ".so"
            addarflags = ""
        makefile_inc.extend([
            'LIB       = %s' % libext,
            'CLIBFLAGS = -shared -fPIC',
            'RANLIB    = echo',
            'AR        = $(CC)',
            'ARFLAGS   = -shared $(LDFLAGS) %s -o' % addarflags
            ])

    def extra_features(self, makefile_inc, defines):
        ldflags = []

        if '+compression' in self.spec:
            defines.append('-DCOMMON_FILE_COMPRESS_GZ')
            ldflags.append('-L%s -lz' % (self.spec['zlib'].prefix.lib))

        if self.spec.satisfies('+pthread'):
            defines.append('-DCOMMON_PTHREAD')
            defines.append('-DCOMMON_PTHREAD_BARRIER')

        if self.spec.satisfies('+int64'):
            defines.append('-DINTSIZE64')
            defines.append('-DIDXSIZE64')

        if platform.system() == 'Darwin':
            ldflags.append('-lm -pthread')
        else:
            ldflags.append('-lm -lrt -pthread')

        makefile_inc.append('LDFLAGS   = %s' % ' '.join(ldflags))

    def setup(self):

        if self.spec.satisfies('~pthread') and self.spec.satisfies('@6.0.4'):
            sys.exit('Error: SCOTCH 6.0.4 cannot compile without pthread... :(')

        makefile_inc = []
        defines = [
            '-DCOMMON_TIMING_OLD',
            '-DCOMMON_RANDOM_FIXED_SEED',
            '-DSCOTCH_DETERMINISTIC',
            '-DSCOTCH_RENAME'
            ]

        self.library_build_type(makefile_inc, defines)
        self.compiler_specifics(makefile_inc, defines)
        self.extra_features(makefile_inc, defines)

        makefile_inc.extend([
            'EXE       =',
            'OBJ       = .o',
            'MAKE      = make',
            'CAT       = cat',
            'LN        = ln',
            'MKDIR     = mkdir',
            'MV        = mv',
            'CP        = cp',
            'CFLAGS    = -O3 %s' % (' '.join(defines)),
            'LEX       = %s -Pscotchyy -olex.yy.c' % os.path.join(self.spec['flex'].prefix.bin , 'flex'),
            'YACC      = %s -pscotchyy -y -b y' %    os.path.join(self.spec['bison'].prefix.bin, 'bison'),
            'prefix    = %s' % self.prefix,
            ''
            ])

        with working_dir('src'):
            with open('Makefile.inc', 'w') as fh:
                fh.write('\n'.join(makefile_inc))

    def install(self, spec, prefix):
        self.setup()

        targets = ['scotch']
        if self.spec.satisfies('+mpi'):
            targets.append('ptscotch')

        if self.spec.satisfies('+esmumps') and spec.satisfies('@6:'):
            # No 'make esmumps ptesmumps' in scotch_5.1.11_esmumps.tar.gz
            targets.append('esmumps')
            if self.spec.satisfies('+mpi'):
                targets.append('ptesmumps')

        with working_dir('src'):
            for app in targets:
                make(app, parallel=0)

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('man/man1', prefix.share_man1)
        if spec.satisfies('+grf'):
            with working_dir('grf'):
                for f in os.listdir('.'):
                    gunzip(f)
            install_tree('grf', prefix + '/grf')
