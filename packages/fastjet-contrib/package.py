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


class FastjetContrib(AutotoolsPackage):
    """."""

    homepage = "http://www.example.com"
    url = "https://github.com/cms-externals/fastjet-contrib"

    version('1.026', git='https://github.com/cms-externals/fastjet-contrib', branch='cms/v1.026')

    depends_on('fastjet')

    def configure_args(self):
        args = ['--fastjet-config=%s/fastjet-config' %
                self.spec['fastjet'].prefix.bin,
                'CXXFLAGS=-I%s' % self.spec['fastjet'].prefix.include]
        return args

    def install(self, spec, prefix):
        make()
        make('check')
        make('install')
        make('fragile-shared')
        make('fragile-shared-install')

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

        fname = 'fastjet-contrib.xml'
        template = Template("""
  <tool name="fastjet-contrib" version="${VER}">
    <info url="http://fastjet.hepforge.org/contrib/"/>
    <lib name="fastjetcontribfragile"/>
    <client>
      <environment name="FASTJET_CONTRIB_BASE" default="${PFX}"/>
      <environment name="LIBDIR" default="$$FASTJET_CONTRIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$FASTJET_CONTRIB_BASE/include"/>
    </client>
  </tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
