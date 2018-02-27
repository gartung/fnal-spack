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
from contextlib import closing


class TcmallocFake(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/google-perftools/1.6-giojec2/google-perftools-1.6.tar.gz"

    version('1.6', '7acfee8d3e2ba968d20684e9f7033015')

    def install(self, spec, prefix):
        comp = which('g++')
        with closing(open('tmpgp.cc', 'w')) as f:
            f.write("""
namespace gptmp {
  void foo(void*) {
  }
}
""")
        comp('-c', '-o', 'tmp.o', '-fPIC', 'tmpgp.cc')
        comp('-shared', '-o', 'libgptmp.so', 'tmp.o')
        mkdirp('%s' % prefix.lib)
        install('libgptmp.so', '%s/libtcmalloc.so' % prefix.lib)
        install('libgptmp.so', '%s/libtcmalloc_minimal.so' % prefix.lib)

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

        fname = 'tcmalloc_minimal.xml'
        template = Template("""<tool name="tcmalloc_minimal" version="$VER">
  <lib name="tcmalloc_minimal"/>
  <client>
    <environment name="TCMALLOC_MINIMAL_BASE" default="$PFX"/>
    <environment name="LIBDIR"                default="$$TCMALLOC_MINIMAL_BASE/lib"/>
  </client>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'tcmalloc.xml'
        template = Template("""<tool name="tcmalloc" version="$VER">
  <lib name="tcmalloc"/>
  <client>
    <environment name="TCMALLOC_BASE" default="$PFX"/>
    <environment name="LIBDIR"        default="$$TCMALLOC_BASE/lib"/>
  </client>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
