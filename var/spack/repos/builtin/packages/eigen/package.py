##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by David Beckingsale, david@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *


class Eigen(Package):
    """
    Eigen is a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms
    """

    homepage = 'http://eigen.tuxfamily.org/'
    url = 'http://bitbucket.org/eigen/eigen/get/3.2.7.tar.bz2'

    version('3.2.7', 'cc1bacbad97558b97da6b77c9644f184', url='http://bitbucket.org/eigen/eigen/get/3.2.7.tar.bz2')

    variant('debug', default=False, description='Builds the library in debug mode')

    variant('metis', default=True, description='Enables metis backend')
    variant('scotch', default=True, description='Enables scotch backend')
    variant('fftw', default=True, description='Enables FFTW backend')
    variant('suitesparse', default=True, description='Enables SuiteSparse support')

    # TODO : dependency on googlehash, superlu, adolc missing

    depends_on('metis@5:', when='+metis')
    depends_on('scotch', when='+scotch')
    depends_on('fftw', when='+fftw')
    depends_on('suite-sparse', when='+suitesparse')
    depends_on('mpfr@2.3.0:')  # Eigen 3.2.7 requires at least 2.3.0
    depends_on('gmp')

    def install(self, spec, prefix):

        options = []
        options.extend(std_cmake_args)

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')

        with working_dir(build_directory, create=True):
            cmake(source_directory, *options)
            make()
            make("install")
