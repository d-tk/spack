from spack import *
import os

class Paraview(Package):
    homepage = 'http://www.paraview.org'
    url      = 'http://www.paraview.org/files/v5.0/ParaView-v'
    _url_str = 'http://www.paraview.org/files/v%s/ParaView-v%s-source.tar.gz'

    version('4.4.0', 'fa1569857dd680ebb4d7ff89c2227378')
    version('5.0.0', '4598f0b421460c8bbc635c9a1c3bdbee')
    version('5.0.1', 'fdf206113369746e2276b95b257d2c9b')

    variant('python', default=False, description='Enable Python support')

    variant('tcl', default=False, description='Enable TCL support')

    variant('mpi', default=False, description='Enable MPI support')

    variant('osmesa', default=False, description='Enable OSMesa support')
    variant('qt', default=False, description='Enable Qt support')
    variant('qt5', default=False, description='Enable Qt 5 support')
    variant('opengl2', default=False, description='Enable OpenGL2 backend')

    depends_on('python@2:2.7', when='+python')
    depends_on('py-numpy', when='+python')
    depends_on('py-matplotlib', when='+python')
    depends_on('tcl', when='+tcl')
    depends_on('mpi', when='+mpi')
    depends_on('qt@:4', when='+qt')
    depends_on('qt@5.0.0:', when='+qt5')

    depends_on('bzip2')
    depends_on('freetype')
    # depends_on('hdf5+mpi', when='+mpi')
    # depends_on('hdf5~mpi', when='~mpi')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('netcdf')
    #depends_on('protobuf') # version mismatches?
    #depends_on('sqlite') # external version not supported
    depends_on('zlib')

    def validate(self, spec):
        """
        Checks if incompatible variants have been activated at the same time

        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        if '+qt' in spec and  '+qt5' in spec:
            msg = 'cannot use both qt and qt5 variant'
            raise RuntimeError(msg)

    def url_for_version(self, version):
        """Handle ParaView version-based custom URLs."""
        return self._url_str % (version.up_to(2), version)


    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            def feature_to_bool(feature, on='ON', off='OFF'):
                if feature in spec:
                    return on
                return off

            def nfeature_to_bool(feature):
                return feature_to_bool(feature, on='OFF', off='ON')

            feature_args = std_cmake_args[:]
            feature_args.append('-DPARAVIEW_BUILD_QT_GUI:BOOL=%s' % feature_to_bool('+qt'))
            feature_args.append('-DPARAVIEW_BUILD_QT_GUI:BOOL=%s' % feature_to_bool('+qt5'))
            feature_args.append('-DPARAVIEW_ENABLE_PYTHON:BOOL=%s' % feature_to_bool('+python'))
            if '+python' in spec:
                feature_args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s/bin/python' % spec['python'].prefix)
            feature_args.append('-DPARAVIEW_USE_MPI:BOOL=%s' % feature_to_bool('+mpi'))
            if '+mpi' in spec:
                feature_args.append('-DMPIEXEC:FILEPATH=%s/bin/mpiexec' % spec['mpi'].prefix)
            feature_args.append('-DVTK_ENABLE_TCL_WRAPPING:BOOL=%s' % feature_to_bool('+tcl'))
            feature_args.append('-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' % feature_to_bool('+osmesa'))
            feature_args.append('-DVTK_USE_X:BOOL=%s' % nfeature_to_bool('+osmesa'))
            feature_args.append('-DVTK_RENDERING_BACKEND:STRING=%s' % feature_to_bool('+opengl2', 'OpenGL2', 'OpenGL'))

            # feature_args.append("-DHDF5_DIR=%s" % spec['hdf5'].prefix )
            # feature_args.append("-DHDF5_IS_PARALLEL=%s" % feature_to_bool('+mpi'))
            # feature_args.append("-DHDF5_HL_LIBRARY:FILEPATH=%s" % spec['hdf5'].prefix.lib+"/libhdf5_hl.so")
            if spec['qt'].satisfies('@5'):
                feature_args.append("-DPARAVIEW_QT_VERSION:STRING=5")

            feature_args.extend(std_cmake_args)

            if 'darwin' in self.spec.architecture:
                feature_args.append('-DVTK_USE_X:BOOL=OFF')
                feature_args.append('-DPARAVIEW_DO_UNIX_STYLE_INSTALLS:BOOL=ON')

#            os.environ['HDF5_ROOT'] = spec['hdf5'].prefix
            cmake('..',
                '-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix,
                '-DBUILD_TESTING:BOOL=OFF',
                '-DVTK_USE_SYSTEM_FREETYPE:BOOL=ON',
                '-DVTK_USE_SYSTEM_HDF5:BOOL=OFF',
                '-DVTK_USE_SYSTEM_JPEG:BOOL=ON',
                '-DVTK_USE_SYSTEM_LIBXML2:BOOL=ON',
                '-DVTK_USE_SYSTEM_NETCDF:BOOL=ON',
                '-DVTK_USE_SYSTEM_TIFF:BOOL=ON',
                '-DVTK_USE_SYSTEM_ZLIB:BOOL=ON',
                *feature_args)
            make()
            make('install')
