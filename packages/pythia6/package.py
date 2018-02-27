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
from spack import *
import distutils.dir_util as du

class Pythia6(Package):
    """PYTHIA is a program for the generation of high-energy physics events,
    i.e. for the description of collisions at high energies between elementary
    particles such as e+, e-, p and pbar in various combinations."""

    homepage = "https://pythia6.hepforge.org/"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz"

    version('426', '4dd75f551b7660c35f817c063abd74ca91b70259c0987905a06ebb2d21bcdf26')

    def install(self, spec, prefix):
        with working_dir(self.version.string):
            configure('--with-hepevt=4000')
            make()
            make('install')
            du.copy_tree('lib',prefix.lib)
            du.copy_tree('include',prefix.include)

    def url_for_version(self,version):
        url='http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz'%self.version
        return url


    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):

        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'pythia6_headers.xml'
        template = Template("""
<tool name="pythia6_headers" version="${VER}">
  <client>
    <environment name="PYTHIA6_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PYTHIA6_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'pythia6.xml'
        template = Template("""
<tool name="pythia6" version="${VER}">
  <lib name="pythia6"/>
  <lib name="pythia6_dummy"/>
  <lib name="pythia6_pdfdummy"/>
  <client>
    <environment name="PYTHIA6_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PYTHIA6_BASE/lib"/>
  </client>
  <use name="pythia6_headers"/>
  <use name="f77compiler"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'pydata.xml'
        template = Template("""
<tool name="pydata" version="${VER}">
  <client>
    <environment name="PYDATA_BASE" default="${PFX}"/>
  </client>
  <architecture name="slc.*|fc.*|linux*">
    <flags LDFLAGS="$$(PYDATA_BASE)/lib/pydata.o"/>
  </architecture>
  <flags NO_RECURSIVE_EXPORT="1"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
