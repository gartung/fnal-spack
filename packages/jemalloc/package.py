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


class Jemalloc(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "https://github.com/jemalloc/jemalloc/archive/5.0.1.tar.gz"

    version('4.2.1', '25a6f63d88cabfd7f0f98a4f2f469ba7')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')


    def autoreconf(self, spec, prefix):
        bash=which('bash')
        bash('autogen.sh')

    def install(self, spec, prefix):
        make()
        make('doc/jemalloc.3')
        make('doc/jemalloc.html')
        make('install')

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

        fname = 'jemalloc.xml'
        template = Template("""
<tool name="jemalloc" version="${VER}">
  <architecture name="slc.*|fc.*|linux*">
    <lib name="jemalloc"/>
  </architecture>
  <client>
    <environment name="JEMALLOC_BASE" default="${PFX}"/>
    <environment name="LIBDIR"        default="$$JEMALLOC_BASE/lib"/>
    <environment name="INCLUDE"        default="$$JEMALLOC_BASE/include"/>
  </client>
  <runtime name="MALLOC_CONF" value="lg_chunk:18,lg_dirty_mult:4"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
