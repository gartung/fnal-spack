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
        args = ['%s/cetpkgsupport' % self.stage.path]
        args += ['-DCMAKE_INSTALL_PREFIX=%s'%self.prefix]
        cmake=which('cmake')
        ups=which('ups')
        setups='%s/db/setup'%self.spec['ups'].prefix
        sfd='%s/cetpkgsupport/ups/setup_for_development'%self.stage.path
        bash=which('bash')
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            bash('-c','source %s;source %s;env'%(setups,sfd),output=str,error=str)
            cmake(*args)
            make()
            make('install')
        ups=which('ups')
        flavor=ups('flavor',output=str)
        flvr=flavor.strip('\n')
        ups('declare','cetpkgsupport','%s'%spec.version,'-f',flvr,'-r','%s'%prefix,'-m','%s/cetpkgsupport/%s/ups/cetpkgsupport.table'%(prefix,spec.version),'-C','-z','%s/db'%spec['ups'].prefix)
        ups('declare','cetpkgsupport','%s'%spec.version,'-f',flvr,'-4','-C','-c','-z','%s/db'%spec['ups'].prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', '%s/cetpkgsupport/%s/bin'%(self.prefix,self.spec.version))
        spack_env.prepend_path('PATH', '%s/cetpkgsupport/%s/bin'%(self.prefix,self.spec.version))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        run_env.prepend_path('PATH', '%s/cetpkgsupport/%s/bin'%(self.prefix,self.spec.version))
        spack_env.prepend_path('PATH', '%s/cetpkgsupport/%s/bin'%(self.prefix,self.spec.version))

