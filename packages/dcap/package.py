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


class Dcap(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/cms-externals/dcap/archive/2.47.8.tar.gz"

    version('2.47.8', '8dfa5b3d665a7c950050b05576c59d8e')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # FIXME: Add additional dependencies if required.
    depends_on('zlib')

    def autoreconf(self, spec, prefix):
        filter_file(r'library_includedir.*', 
                   'library_includedir=$(includedir)',
                   'src/Makefile.am')
        mkdirp('config')
        aclocal('-I', 'config')
        autoheader()
        libtoolize('--automake')
        automake('--add-missing', '--copy', '--foreign')
        autoconf()

    def configure_args(self):
        args = ['CFLAGS=-I%s' % self.spec['zlib'].prefix.include,
                'LDFLAGS=-L%s' % self.spec['zlib'].prefix.lib ]
        return args

    def install(self, spec, prefix):
        make('-C', 'src')
        make('-C', 'src', 'install')

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

        fname = 'dcap.xml'
        template = Template("""
<tool name="dcap" version="${VER}">
  <lib name="dcap"/>
  <client>
    <environment name="DCAP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$DCAP_BASE/lib"/>
    <environment name="INCLUDE" default="$$DCAP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

