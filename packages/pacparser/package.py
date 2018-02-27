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


class Pacparser(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "https://github.com/manugarg/pacparser/releases/download/1.3.5/pacparser-1.3.5.tar.gz"

#    version('1.3.7', 'ca716d7a0c73df868cd0c1358b21c3fd')
    version('1.3.5', '9db90bd4d88dfd8d31fa707466259566')
#    version('1.3.3', 'e5d2e0a347654ab35b3ff1f4c87f5ff3')


    def install(self, spec, prefix):
        make('-C', 'src', 'PREFIX=%s' % prefix)
        make('-C', 'src', 'install', 'PREFIX=%s' % prefix)

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

        fname = 'pacparser.xml'
        template = Template("""<tool name="pacparser" version="$VER">
  <info url="http://code.google.com/p/pacparser/"/>
  <lib name="pacparser"/>
  <client>
    <environment name="PACPARSER_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$PACPARSER_BASE/lib"/>
    <environment name="INCLUDE" default="$$PACPARSER_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$PACPARSER_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
