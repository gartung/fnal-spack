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
#     spack install cetbuildtools
#
# You can edit this file again by typing:
#
#     spack edit cetbuildtools
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
from spack.environment import *

class Cetbuildtools(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    #homepage = "http://www.example.com"
    #url      = "http://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('v5_07_00', git='http://cdcvs.fnal.gov/projects/cetbuildtools',tag='v5_07_00')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('ups')
    depends_on('cetpkgsupport')
    depends_on('cmake')

    def install(self,spec,prefix):
        args = ['%s/cetbuildtools' % self.stage.path]
        args += ['-DCMAKE_INSTALL_PREFIX=%s'%self.prefix]
        cmake=which('cmake')
        ups=which('ups')
        setups='%s/db/setup'%self.spec['ups'].prefix
        sfd='%s/cetbuildtools/ups/setup_for_development'%self.stage.path
        bash=which('bash')
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            bash('-c','source %s;source %s;env'%(setups,sfd),output=str)
            setupenv=EnvironmentModifications()
            setupenv.set('CETBUILDTOOLS_DIR','%s/cetbuildtools'%self.stage.path)
            setupenv.append_path('PATH','%s/cetbuildtools/bin'%self.stage.path)
            setupenv.apply_modifications()
            cmake(*args)
            make()
            make('install')
        ups=which('ups')
        flavor=ups('flavor',output=str)
        flvr=flavor.strip('\n')
        ups('declare','cetbuildtools','%s'%spec.version,'-f',flvr,'-r','%s'%prefix,'-m','%s/cetbuildtools/%s/ups/cetbuildtools.table'%(prefix,spec.version),'-C','-z','%s/db'%spec['ups'].prefix)
        ups('declare','cetbuildtools','%s'%spec.version,'-f',flvr,'-4','-C','-c','-z','%s/db'%spec['ups'].prefix)


    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', '%s/cetbuildtools/%s/bin'%(self.prefix,self.spec.version))
        spack_env.prepend_path('PATH', '%s/cetbuildtools/%s/bin'%(self.prefix,self.spec.version))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        run_env.prepend_path('PATH', '%s/cetbuildtools/%s/bin'%(self.prefix,self.spec.version))
        spack_env.prepend_path('PATH', '%s/cetbuildtools/%s/bin'%(self.prefix,self.spec.version))

