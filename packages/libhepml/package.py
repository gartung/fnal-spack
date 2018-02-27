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
import glob


class Libhepml(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "http://mcdb.cern.ch/distribution/api/libhepml-0.2.1.tar.gz"

    version('0.2.6',    'e414906a3e475cd7e5bdb6119fea15c1')
    version('0.2.5',    'c34d2155002f47de76728516a940f881')
    version('0.2.3ext', 'c17ea60f8bf93bfea7cc14bb57b0a0a1')
    version('0.2.3',    '29120e56c2bcbd59425fee82f7fdb5a1')
    version('0.2.2',    '76f3d5458252e67476dd661685e9983d')
    version('0.2.1',    '646964f8478fe0d64888514a8a1d8d19', preferred=True)

    patch('libhepml-0.2.1-gcc43.patch', level=2)

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        with working_dir('src'):
            make()
            for f in glob.glob('*.so'):
                install(f, join_path(prefix.lib, f))
        install_tree('interface', join_path(prefix, 'interface'))

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

        fname = 'libhepml.xml'
        template = Template("""
<tool name="libhepml" version="${VER}">
  <lib name="hepml"/>
  <client>
    <environment name="LIBHEPML_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LIBHEPML_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBHEPML_BASE/interface"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
