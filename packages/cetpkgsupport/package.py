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
#     spack install cetpkgsupport
#
# You can edit this file again by typing:
#
#     spack edit cetpkgsupport
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Cetpkgsupport(Package):

    version('v1_11_00', git='http://cdcvs.fnal.gov/projects/cetpkgsupport',tag='v1_11_00')
    version('v1_10_02', git='http://cdcvs.fnal.gov/projects/cetpkgsupport',tag='v1_10_02')
    version('v1_10_01', git='http://cdcvs.fnal.gov/projects/cetpkgsupport',tag='v1_10_01')


    depends_on('cmake')
    depends_on('ups')

    def install(self,spec,prefix):
        setups='%s/../../../products/setup'%spec['ups'].prefix
        sfd='%s/%s/ups/setup_for_development'%(self.stage.path,spec.name)
        bash=which('bash')
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            output=bash('-c','source %s && source %s && cmake %s/%s -DCMAKE_INSTALL_PREFIX=%s '%(setups,sfd,self.stage.path,spec.name,prefix),output=str,error=str)
            print output
            make('VERBOSE=1')
            make('install')
        ln=which('ln')
        mkdirp('%s/../../../products/%s'%(spec.name,prefix))
        ln('-s','%s/%s/%s'%(prefix,spec.name,spec.version),'%s/../../../products/%s'%(prefix,spec.name))
        ln('-s','%s/%s/%s.version'%(prefix,spec.name,spec.version),'%s/../../../products/%s'%(prefix,spec.name))
        ln('-s','%s/%s/current.chain'%(prefix,spec.name),'%s/../../../products/%s'%(prefix,spec.name))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', '%s/%s/%s/bin'%(prefix,self.spec.name,self.spec.version))
        spack_env.prepend_path('PATH', '%s/%s/%s/bin'%(prefix,self.spec.name,self.spec.version))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        run_env.prepend_path('PATH', '%s/%s/%s/bin'%(self.prefix,self.spec.name,self.spec.version))
        spack_env.prepend_path('PATH', '%s/%s/%s/bin'%(self.prefix,self.spec.name,self.spec.version))

