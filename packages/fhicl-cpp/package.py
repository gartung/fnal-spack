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
#     spack install fhicl-cpp
#
# You can edit this file again by typing:
#
#     spack edit fhicl-cpp
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import os


class FhiclCpp(Package):
    homepage='http://cdcvs.fnal.gov/projects/fhicl-cpp',

    version(
        'v4_04_00',
        git='http://cdcvs.fnal.gov/projects/fhicl-cpp',
        tag='v4_04_00')

    version(
        'v4_03_02',
        git='http://cdcvs.fnal.gov/projects/fhicl-cpp',
        tag='v4_03_02')

    depends_on("ups", type="build")
    depends_on("cmake", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("cetlib")
    depends_on("ups-boost-table")
    depends_on("ups-sqlite-table")
    depends_on("ups-openssl-table")

    def install(self,spec,prefix):
        mkdirp('%s'%prefix)
        rsync=which('rsync')
        rsync('-a', '-v', '%s'%self.stage.source_path, '%s'%prefix)

    def realinstall(self, spec, prefix):
        setups = '%s/../products/setup' % spec['ups'].prefix
        sfd = '%s/%s/ups/setup_for_development -p ' % (
            self.stage.path, spec.name)
        bash = which('bash')
        cmake_cmd = 'source %s ' % setups + '&& source %s ' % sfd + \
            '&& cmake %s' % self.stage.source_path + \
            ' -DCMAKE_INSTALL_PREFIX=%s' % prefix + \
            ' -DCMAKE_BUILD_TYPE=${CETPKG_TYPE} -DCMAKE_CXX_FLAGS=-std=c++14'
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            output = bash(
                '-c', cmake_cmd,
                output=str,
                error=str)
            print output
            make('VERBOSE=1')
            make('install')
        name_ = str(spec.name).replace('-', '')
        dst = '%s/../products/%s' % (spec['ups'].prefix, name_)
        mkdirp(dst)
        src1 = join_path(prefix, name_, spec.version)
        src2 = join_path(prefix, name_, '%s.version' % spec.version)
        dst1 = join_path(dst, spec.version)
        dst2 = join_path(dst, '%s.version' % spec.version)
        if os.path.exists(dst1):
            print 'symbolic link %s already exists' % dst1
        else:
            os.symlink(src1, dst1)
        if os.path.exists(dst2):
            print 'symbolic link %s already exists' % dst2
        else:
            os.symlink(src2, dst2)
#        ln = which('ln')
#        ln('-s', '%s/%s/%s/*/lib' %
#           (prefix, name_, spec.version), '%s' %
#            prefix)
#        ln('-s', '%s/%s/%s/include' %
#           (prefix, name_, spec.version), '%s' %
#            prefix)
