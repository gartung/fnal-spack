##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Vdt(CMakePackage):
    """Vectorised math. A collection of fast and inline implementations of
    mathematical functions."""

    homepage = "https://github.com/dpiparo/vdt"
    url = "https://github.com/dpiparo/vdt/archive/v0.3.9.tar.gz"

    version('0.3.9', '80a2d73a82f7ef8257a8206ca22dd145')
    version('0.3.8', '25b07c72510aaa95fffc11e33579061c')
    version('0.3.7', 'd2621d4c489894fd1fe8e056d9a0a67c')
    version('0.3.6', '6eaff3bbbd5175332ccbd66cd71a741d')

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

        fname = 'vdt_headers.xml'
        template = Template("""<tool name="vdt_headers" version="$VER">
  <client>
    <environment name="VDT_HEADERS_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$VDT_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'vdt.xml'
        template = Template("""<tool name="vdt" version="$VER">
  <lib name="vdt"/>
  <use name="vdt_headers"/>
  <client>
    <environment name="VDT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$VDT_BASE/lib"/>
  </client>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
