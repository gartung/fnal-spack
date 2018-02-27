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


class Davix(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "https://github.com/cern-it-sdc-id/davix/archive/R_0_6_5.tar.gz"

    version('0_6_5', 'a7f09dfa0bd0daaa46aafc8e0f4b1a25')

    depends_on('libxml2+python')
    depends_on('boost+python')
    depends_on('cmake', type='build')

    def cmake_args(self):
        args = ['-DLIBXML2_INCLUDE_DIR=%s/include/libxml2' % self.spec['libxml2'].prefix,
                '-DLIBXML2_LIBRARIES=%s/lib/libxml2.%s' %
                (self.spec['libxml2'].prefix, dso_suffix),
                '-DBoost_NO_SYSTEM_PATHS:BOOL=TRUE',
                '-DBOOST_ROOT:PATH=%s' % self.spec['boost'].prefix,
                '-DOPENSSL_ROOT_DIR=%s' % self.spec['openssl'].prefix]
        return args

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
        values['LIB'] = self.spec.prefix.lib64

        fname = 'davix.xml'
        template = Template("""<tool name="davix" version="$VER">
    <info url="https://dmc.web.cern.ch/projects/davix/home"/>
    <lib name="davix"/>
    <client>
      <environment name="DAVIX_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$LIB"/>
      <environment name="INCLUDE" default="$$DAVIX_BASE/include/davix"/>
    </client>
    <runtime name="PATH" value="$$DAVIX_BASE/bin" type="path"/>
    <use name="boost_system"/>
    <use name="openssl"/>
    <use name="libxml2"/>
  </tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
