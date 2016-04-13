from spack import *

class Cgal(Package):
    """CGAL is a software project that provides easy access to efficient
    and reliable geometric algorithms in the form of a C++ library. CGAL
    is used in various areas needing geometric computation, such as
    geographic information systems, computer aided design, molecular
    biology, medical imaging, computer graphics, and robotics."""

    homepage = "http://www.cgal.org/index.html"
    url      = "https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-4.7/CGAL-4.7.tar.gz"

    version('releases%2FCGAL-4.7', '6198fd4a4926add422a189a420cdd8cb')

    depends_on("gmp")
    depends_on("mpfr")

    def install(self, spec, prefix):

        with working_dir('spack-build', create=True):

            cmake_args = [".."]
            cmake_args.extend(std_cmake_args)
            cmake_args.extend(['-DCMAKE_BUILD_TYPE=Release'])

            cmake_args.extend(['-DWITH_CGAL_Qt3=OFF'])
            cmake_args.extend(['-DWITH_CGAL_Qt5=OFF'])

            cmake_args.extend(['-DGMP_INCLUDE_DIR=%s' % spec['gmp'].prefix.include])
            cmake_args.extend(['-DGMP_LIBRARIES_DIR=%s' % spec['gmp'].prefix.lib])

            cmake_args.extend(['-DMPFR_INCLUDE_DIR=%s' % spec['mpfr'].prefix.include])
            cmake_args.extend(['-DMPFR_LIBRARIES_DIR=%s' % spec['mpfr'].prefix.lib])

            cmake(*cmake_args)

            make()
            make('install')
