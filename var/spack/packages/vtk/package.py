from spack import *

class Vtk(Package):
    """The Visualization Toolkit (VTK) is an open-source, freely
    available software system for 3D computer graphics, image
    processing and visualization. """
    homepage = "http://www.vtk.org"
    url      = "http://www.vtk.org/files/release/6.1/VTK-6.1.0.tar.gz"

    version('6.3.0', '0231ca4840408e9dd60af48b314c5b6d', url="http://www.vtk.org/files/release/6.3/VTK-6.3.0.tar.gz")
    version('6.2.0', '4790f8b3acdbc376997fbdc9d203f0b7', url="http://www.vtk.org/files/release/6.2/VTK-6.2.0.tar.gz")
    version('6.1.0', '25e4dfb3bad778722dcaec80cd5dab7d')

    variant('opengl2', default=False, description='Enable OpenGL2 backend')
    variant('tbb', default=False, description='Enable SMP implementation using TBB')
    variant('openmp', default=False, description='Enable SMP implementation using OpenMP')

    depends_on("qt")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = [
                "..",
                "-DBUILD_SHARED_LIBS=ON",
                # Disable wrappers for other languages.
                "-DVTK_WRAP_PYTHON=OFF",
                "-DVTK_WRAP_JAVA=OFF",
                "-DVTK_WRAP_TCL=OFF"]
            cmake_args.extend(std_cmake_args)

            # Enable Qt support here.
            cmake_args.extend([
                "-DQT_QMAKE_EXECUTABLE:PATH=%s/qmake" % spec['qt'].prefix.bin,
                "-DVTK_Group_Qt:BOOL=ON",
                # Ignore webkit because it's hard to build w/Qt
                "-DVTK_Group_Qt=OFF",
                "-DModule_vtkGUISupportQt:BOOL=ON",
                "-DModule_vtkGUISupportQtOpenGL:BOOL=ON"
                ])
            if spec.satisfies('+opengl2'):
                cmake_args.append("-D VTK_RENDERING_BACKEND:STRING=OpenGL2")

            if spec.satisfies('+tbb'):
                cmake_args.append("-DVTK_SMP_IMPLEMENTATION_TYPE:STRING=TBB")
            if spec.satisfies('+openmp'):
                cmake_args.append("-DVTK_SMP_IMPLEMENTATION_TYPE:STRING=OpenMP")

            if spec['qt'].satisfies('@5'):
                cmake_args.append("-DVTK_QT_VERSION:STRING=5")

            cmake(*cmake_args)
            make()
            make("install")
