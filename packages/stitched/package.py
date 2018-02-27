##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install stitched
#
# You can edit this file again by typing:
#
#     spack edit stitched
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import os


class Stitched(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('8.0.X', git='https://github.com/gartung/stitched.git',
            commit='8ce0c76', submodules='True')

    # FIXME: Add dependencies if required.
    depends_on('boost+python')
    depends_on('python')
    depends_on('tinyxml')
    depends_on('md5')
    depends_on('root')
    depends_on('castor')
    depends_on('clhep')
    depends_on('tbb')
    depends_on('cppunit')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = ['-DCMakeTools_DIR=%s/cmaketools' % self.stage.source_path]
        args.append('-DCLHEP_ROOT_DIR=%s' % self.spec['clhep'].prefix)
        args.append('-DCASTOR_INCLUDE_DIR=%s/include' %
                    self.spec['castor'].prefix)
        args.append('-DBOOST_ROOT=%s' % self.spec['boost'].prefix)
        args.append('-DTBB_ROOT_DIR=%s' % self.spec['tbb'].prefix)
        args.append('-DTINYXMLROOT=%s' % self.spec['tinyxml'].prefix)
        args.append('-DMD5ROOT=%s' % self.spec['md5'].prefix)
        args.append('-DCPPUNITROOT=%s' % self.spec['cppunit'].prefix)
        return args
