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
from spack import *
import os


class Canvas(Package):
    version(
        'v1_06_02',
        git='http://cdcvs.fnal.gov/projects/canvas',
        tag='v1_06_02')

    depends_on("ups", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("cmake", type="build")
    depends_on("cetlib-except")
    depends_on("cetlib")
    depends_on("fhicl-cpp")
    depends_on("messagefacility")
    depends_on("boost")
    depends_on("sqlite")
    depends_on("openssl")
    depends_on("tbb")

    def install(self, spec, prefix):
        cmake = which('cmake')
        ups = which('ups')
        setups = '%s/../products/setup' % spec['ups'].prefix
        sfd = '%s/%s/ups/setup_for_development -p ' % (
            self.stage.path, spec.name)
        bash = which('bash')
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            output = bash(
                '-c',
                'source %s && source %s && cmake %s/%s -DCMAKE_INSTALL_PREFIX=%s -DCMAKE_BUILD_TYPE=${CETPKG_TYPE} -DCMAKE_CXX_FLAGS=-std=c++14 ' %
                (setups,
                 sfd,
                 self.stage.path,
                 spec.name,
                 self.prefix),
                output=str,
                error=str)
            print output
            make('VERBOSE=1')
            make('install')
        name_ = str(spec.name)
        print name_
        dst = '%s/../products/%s' % (prefix, name_)
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
        ln = which('ln')
        ln('-s', '%s/%s/%s/*/lib' %
           (prefix, name_, spec.version), '%s' %
            prefix)
        ln('-s', '%s/%s/%s/include' %
           (prefix, name_, spec.version), '%s' %
            prefix)
