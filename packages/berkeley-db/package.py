##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class BerkeleyDb(AutotoolsPackage):
    """Oracle Berkeley DB"""

    homepage = "http://www.oracle.com/technetwork/database/database-technologies/berkeleydb/overview/index.html"
    url = "http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz"

    version('6.0.35', 'c65a4d3e930a116abaaf69edfc697f25')
    version('6.1.29', '7f4d47302dfec698fe088e5285c9098e')
    version('6.2.32', '33491b4756cb44b91c3318b727e71023')

    configure_directory = 'dist'
    build_directory = 'spack-build'

    def url_for_version(self, version):
        # newer version need oracle login, so get them from gentoo mirror
        return 'http://distfiles.gentoo.org/distfiles/db-{0}.tar.gz'.format(version)

    def configure_args(self):
        args = ['--disable-static', '--enable-cxx',
                '--enable-stl', '--disable-java', '--disable-tcl']
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
        import sys
        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'db6.xml'
        template = Template("""
<tool name="db6" version="${VER}">
  <lib name="db"/>
  <client>
    <environment name="DB6_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$DB6_BASE/lib"/>
    <environment name="INCLUDE" default="$$DB6_BASE/include"/>
    <environment name="BINDIR" default="$$DB6_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

