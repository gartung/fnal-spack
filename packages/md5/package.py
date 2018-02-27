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
import sys


class Md5(Package):
    """."""

    homepage = "https://github.com/cms-externals/md5"
    url = "http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/md5/1.0.0-giojec/md5.1.0.0-d97a571864a119cd5408d2670d095b4410e926cc.tgz"

    version('1.0.0', 'b154f78e89a70ac1328099d9c3820d13',
            url='http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/md5/1.0.0-giojec/md5.1.0.0-d97a571864a119cd5408d2670d095b4410e926cc.tgz')

    def install(self, spec, prefix):
        comp = which('gcc')
        cp = which('cp')
        md = which('mkdir')
        md('%s' % prefix.lib)
        md('%s' % prefix.include)
        if sys.platform == 'darwin':
            comp('md5.c', '-shared', '-fPIC', '-o', 'libcms-md5.dylib')
            cp('-v', 'libcms-md5.dylib', prefix.lib)
            fix_darwin_install_name(prefix.lib)
        else:
            comp('md5.c', '-shared', '-fPIC', '-o', 'libcms-md5.so')
            cp('-v', 'libcms-md5.so', prefix.lib)
        cp('-v', 'md5.h', prefix.include)

    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'md5.xml'
        template = Template("""<tool name="md5" version="$VER">
  <info url="https://tls.mbed.org/md5-source-code"/>
   <lib name="cms-md5"/>
  <client>
    <environment name="MD5_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$MD5_BASE/lib"/>
    <environment name="INCLUDE" default="$$MD5_BASE/include"/>
    </client>  
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
