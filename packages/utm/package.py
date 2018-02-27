##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Utm(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "https://gitlab.cern.ch/cms-l1t-utm/utm/repository/utm_0.6.5/archive.tar.gz"

    version('0.6.5', git='https://gitlab.cern.ch/cms-l1t-utm/utm.git', tag='utm_0.6.5')

    depends_on('gmake')
    depends_on('xerces-c')
    depends_on('boost')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('XERCES_C_BASE', '%s' % self.spec['xerces-c'].prefix)
        spack_env.set('BOOST_BASE', '%s' % self.spec['boost'].prefix)

    def install(self, spec, prefix):
        make('-f', 'Makefile.standalone', 'all')
        make('-f', 'Makefile.standalone', 'install')
        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)
        install_tree('xsd-type', prefix + '/xds-type')
        install('menu.xsd', prefix + '/menu.xsd')

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

        fname = 'utm.xml'
        template = Template("""
<tool name="utm" version="${VER}">
  <lib name="tmeventsetup"/>
  <lib name="tmtable"/>
  <lib name="tmxsd"/>
  <lib name="tmgrammar"/>
  <lib name="tmutil"/>
  <client>
    <environment name="UTM_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$UTM_BASE/lib"/>
    <environment name="INCLUDE" default="$$UTM_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="UTM_XSD_DIR" value="$$UTM_BASE"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
