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


class Fftjet(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "https://www.hepforge.org/archive/fftjet/fftjet-1.5.0.tar.gz"

    #version('1.5.1', '71ccb59dcb94d83c7e33919db0617656')
    version('1.5.0', '9f91b6974c00ba546833c38d5b3aa563')



    depends_on('fftw')

    def configure_args(self):
        args = ['--disable-dependency-tracking',
                '--enable-threads',
                'CFLAGS=-fpic',
                'DEPS_CFLAGS=-I%s' % self.spec['fftw'].prefix.include,
                'DEPS_LIBS="-L%s -lfftw3"' % self.spec['fftw'].prefix.lib]
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

        fname = 'fftjet.xml'
        template = Template("""<tool name="fftjet" version="$VER">
  <lib name="fftjet"/>
  <client>
    <environment name="FFTJET_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$FFTJET_BASE/lib"/>
    <environment name="INCLUDE" default="$$FFTJET_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
