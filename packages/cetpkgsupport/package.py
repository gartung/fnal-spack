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


class Cetpkgsupport(Package):
    homepage = 'http://cdcvs.fnal.gov/projects/cetpkgsupport'

    version(
        'v1_11_00',
        git='http://cdcvs.fnal.gov/projects/cetpkgsupport',
        tag='v1_11_00')

    version(
        'v1_10_02',
        git='http://cdcvs.fnal.gov/projects/cetpkgsupport',
        tag='v1_10_02')

    version(
        'v1_10_01',
        git='http://cdcvs.fnal.gov/projects/cetpkgsupport',
        tag='v1_10_01')

    depends_on('cmake')
    depends_on('ups')

    def install(self, spec, prefix):
        setups = '%s/../products/setup' % spec['ups'].prefix
        sfd = '%s/%s/ups/setup_for_development' % (self.stage.path, spec.name)
        bash = which('bash')
        ups = which('ups')
        flvr = ups('flavor', output=str).strip('\n')
        output = bash(
            '-c',
            'source ' + setups + ' && %s/bin/product-stub' % self.stage.source_path + ' -f ' +
            flvr + ' cmake v3_3_2 ' +
            '%s' % spec['cmake'].prefix +
            ' %s/../products' % spec['ups'].prefix,
            output=str,
            error=str)
        print output
        build_directory = join_path(self.stage.path, 'spack-build')
        with working_dir(build_directory, create=True):
            output = bash(
                '-c', 'source %s && source %s && cmake %s/%s -DCMAKE_INSTALL_PREFIX=%s ' %
                (setups, sfd, self.stage.path, spec.name, prefix), output=str, error=str)
            print output
            make('VERBOSE=1')
            make('install')
        name_ = str(spec.name)
        print name_
        dst = '%s/../products/%s' % (spec['ups'].prefix, name_)
        mkdirp(dst)
        src1 = join_path(prefix, name_, spec.version)
        src2 = join_path(prefix, name_, '%s.version' % spec.version)
        src3 = join_path(prefix, name_, 'current.chain')
        dst1 = join_path(dst, spec.version)
        dst2 = join_path(dst, '%s.version' % spec.version)
        dst3 = join_path(dst, 'current.chain')
        if os.path.exists(dst1):
            print 'symbolic link %s already exists' % dst1
        else:
            os.symlink(src1, dst1)
        if os.path.exists(dst2):
            print 'symbolic link %s already exists' % dst2
        else:
            os.symlink(src2, dst2)
        if os.path.exists(dst3):
            print 'symbolic link %s already exists' % dst3
        else:
            os.symlink(src3, dst3)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path(
            'PATH', '%s/%s/%s/bin' %
            (prefix, self.spec.name, self.spec.version))
        spack_env.prepend_path(
            'PATH', '%s/%s/%s/bin' %
            (prefix, self.spec.name, self.spec.version))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        run_env.prepend_path('PATH', '%s/%s/%s/bin' %
                             (self.prefix, self.spec.name, self.spec.version))
        spack_env.prepend_path(
            'PATH', '%s/%s/%s/bin' %
            (self.prefix, self.spec.name, self.spec.version))
