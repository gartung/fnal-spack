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
#     spack install cetlib
#
# You can edit this file again by typing:
#
#     spack edit cetlib
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from spack.environment import *

class Cetlib(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    #homepage = "http://www.example.com"
    #url      = "http://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('v2_03_00',git='http://cdcvs.fnal.gov/projects/cetlib', tag='v2_03_00')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    depends_on("cetbuildtools",type="build")
    depends_on("cmake",type="build")
    depends_on("cetlib-except")
    depends_on("boost@1.60.0")
    depends_on("sqlite")
    depends_on("openssl")

    def install(self, spec, prefix):
        cmake=which('cmake')
        ups=which('ups')
        setups='%s/../../../products/setup'%spec['ups'].prefix
        sfd='%s/%s/ups/setup_for_development -p '%(self.stage.path,spec.name)
        bash=which('bash')
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            output=bash('-c','source %s && source %s && cmake %s/%s -DCMAKE_INSTALL_PREFIX=%s -DCMAKE_CXX_FLAGS=-std=c++14'%(setups,sfd,self.stage.path,spec.name,self.prefix),output=str,error=str)
            print output
            make('VERBOSE=1')
            make('install')
        ln=which('ln')
        name_=str(spec.name)
        mkdirp('%s/../../../products/%s'%(prefix,name_))
        ln('-s','%s/%s/%s'%(prefix,name_,spec.version),'%s/../../../products/%s'%(prefix,name_))
        ln('-s','%s/%s/%s.version'%(prefix,name_,spec.version),'%s/../../../products/%s'%(prefix,name_))