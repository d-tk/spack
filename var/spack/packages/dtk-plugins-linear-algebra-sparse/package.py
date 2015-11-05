from spack import *

class DtkPluginsLinearAlgebraSparse(Package):
    """dtk linear algebra sparse plugins of DTK. """
    homepage = "http://dtk.inria.fr/"

    gitroot = "https://github.com/d-tk/dtk-plugins-linear-algebra-sparse.git"
    version('master', git=gitroot, branch = 'master')

    variant('test', default=False, description='Enable test building')
    variant('maphys', default=False, description='Enable maphys plugins')
    variant('hypre', default=False, description='Enable hypre plugins')

    depends_on("dtk-linear-algebra-sparse")
    depends_on("dtk-plugins-distributed")
    depends_on("maphys", when='+maphys')
    depends_on("hypre", when='+hypre')

    def install(self, spec, prefix):


        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DdtkLinearAlgebraSparse_DIR:PATH=%s" % spec['dtk-linear-algebra-sparse'].prefix+"/cmake"
            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+hypre'):
                hypre = spec['hypre'].prefix
                cmake_args.append("-DHYPRE_DIR="+hypre)

            if spec.satisfies('+maphys'):
                maphys = spec['maphys'].prefix
                mversion  = spec['maphys'].format("$@").replace('@','')
                # ugly hack to get the good module directory name
                if mversion == "svn-maphys_0.9.1":
                    mversion = "0.9.2"
                cmake_args.append("-DMAPHYS_INCLUDE_DIR="+maphys+"/include")
                cmake_args.append("-DMAPHYS_LIBRARY_DIR="+maphys+"/lib")
                cmake_args.append("-DMAPHYS_MODULES_DIR="+maphys+"/lib/libmaphys-"+mversion+"_mod")

            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
