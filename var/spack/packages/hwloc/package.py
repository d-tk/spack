from spack import *
import os
import platform

class Hwloc(Package):
    """The Portable Hardware Locality (hwloc) software package
       provides a portable abstraction (across OS, versions,
       architectures, ...) of the hierarchical topology of modern
       architectures, including NUMA memory nodes, sockets, shared
       caches, cores and simultaneous multithreading. It also gathers
       various system attributes such as cache and memory information
       as well as the locality of I/O devices such as network
       interfaces, InfiniBand HCAs or GPUs. It primarily aims at
       helping applications with gathering information about modern
       computing hardware so as to exploit it accordingly and
       efficiently."""
    homepage = "http://www.open-mpi.org/projects/hwloc/"
    url      = "http://www.open-mpi.org/software/hwloc/v1.9/downloads/hwloc-1.9.tar.gz"

    version('1.11.2', '486169cbe111cdea57be12638828ebbf',
            url='http://www.open-mpi.org/software/hwloc/v1.11/downloads/hwloc-1.11.2.tar.bz2')
    version('1.11.1', '002742efd3a8431f98d6315365a2b543',
            url='http://www.open-mpi.org/software/hwloc/v1.11/downloads/hwloc-1.11.1.tar.bz2')
    version('1.9', '1f9f9155682fe8946a97c08896109508')
    version('1.10.1', '27f2966df120a74df19dc244d5340107', url='http://www.open-mpi.org/software/hwloc/v1.10/downloads/hwloc-1.10.1.tar.gz')
    version('1.11.0', '150a6a0b7a136bae5443e9c2cf8f316c', url='http://www.open-mpi.org/software/hwloc/v1.11/downloads/hwloc-1.11.0.tar.gz')

    def install(self, spec, prefix):

        sys_name = platform.system()
        if sys_name == 'Darwin':
            configure("--prefix=%s" % prefix , "--without-x")
        else:
            configure("--prefix=%s" % prefix)

        make()
        make("install")
