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


class Heppdt(AutotoolsPackage):
    """The HepPID library contains translation methods for particle ID's
    to and from various Monte Carlo generators and the PDG standard
    numbering scheme. We realize that the generators adhere closely
    to the standard, but there are occasional differences."""
    homepage = "http://lcgapp.cern.ch/project/simu/HepPDT/"
    url = "http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-2.06.01.tar.gz"

    version('3.04.01', 'a8e93c7603d844266b62d6f189f0ac7e')
    version('3.04.00', '2d2cd7552d3e9539148febacc6287db2')
    version('3.03.02', '0b85f1809bb8b0b28a46f23c718b2773')
    version('3.03.01', 'd411f3bfdf9c4350d802241ba2629cc2')
    version('3.03.00', 'cd84d0a0454be982dcd8c285e060a7b3')
    version('2.06.01', '5688b4bdbd84b48ed5dd2545a3dc33c0')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)

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

        fname = 'heppdt.xml'
        template = Template("""
<tool name="heppdt" version="${VER}">
  <lib name="HepPDT"/>
  <lib name="HepPID"/>
  <client>
    <environment name="HEPPDT_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HEPPDT_BASE/lib"/>
    <environment name="INCLUDE" default="$$HEPPDT_BASE/include"/>
  </client>
  <runtime name="HEPPDT_PARAM_PATH" value="$$HEPPDT_BASE"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
