from spack import *

class Qwt(Package):
    """The Qwt library contains GUI Components and utility classes which are primarily useful for programs with a technical background. Beside a framework for 2D plots it provides scales, sliders, dials, compasses, thermometers, wheels and knobs to control or display values, arrays, or ranges of type double."""

    homepage = "http://qwt.sourceforge.net/"
    url      = "http://pkgs.fedoraproject.org/repo/pkgs/qwt/qwt-6.1.2.tar.bz2/9c88db1774fa7e3045af063bbde44d7d/qwt-6.1.2.tar.bz2"
    # main sourceforge url is:
    # http://sourceforge.net/projects/qwt/files/qwt/6.1.2/qwt-6.1.2.tar.bz2/download

    version('6.1.2', '9c88db1774fa7e3045af063bbde44d7d')

    variant('qt', default=True, description='Add explicit dependancy on qt')

    depends_on("qt@5.0.0:", when="+qt")
    def setup(self):
        qf = FileFilter('qwtconfig.pri')
        qf.filter('/usr/local/qwt-\$\$QWT_VERSION', prefix)

    def install(self, spec, prefix):

        self.setup()
        qmake = which('qmake-qt5')
        if spec.satisfies('+qt'):
            qmake = which("%s/qmake" %spec['qt'].prefix.bin)

        qmake("qwt.pro")
        make()
        make("install")
