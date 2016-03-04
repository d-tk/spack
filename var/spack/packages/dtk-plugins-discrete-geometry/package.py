from spack import *

class DtkPluginsDiscreteGeometry(Package):
    """dtk-plugins-discrete-geometry plugins of DTK. """
    homepage = "http://dtk.inria.fr/"

    gitroot = "https://github.com/d-tk/dtk-plugins-discrete-geometry.git"
    version('master', git=gitroot, branch = 'master')
    version('cgal', git=gitroot, branch = 'cgal')

    variant('test', default=False, description='Enable test building')
    variant('paraview', default=False, description='Enable paraview plugins')
    variant('vtk', default=False, description='Enable VTK plugins')

    depends_on("dtk-discrete-geometry@dev",when='@master')
    depends_on("dtk-discrete-geometry@cgal",when='@cgal')
    depends_on("vtk@6.1.0:",when='+vtk')
    depends_on("paraview",when='+paraview')

    def install(self, spec, prefix):


        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-Ddtk_DIR:PATH=%s" % spec['dtk'].prefix.lib+"/cmake/dtk",
                "-DdtkDiscreteGeometry_DIR:PATH=%s" % spec['dtk-discrete-geometry'].prefix+"/cmake"
            ]
            cmake_args.extend(std_cmake_args)

            if spec.satisfies('+vtk'):
                cmake_args.append("-VTK_DIR=%s" % spec['vtk'].prefix.lib+"/cmake/vtk"+vtk_maj_version )

            if spec.satisfies('+paraview'):
                cmake_args.append("-Paraview_DIR=%s" % spec['paraview'].prefix.lib+"/cmake/paraview"+vtk_maj_version )

            cmake(*cmake_args)
            make()
            if spec.satisfies('+test'):
                make("test")
            make("install")
