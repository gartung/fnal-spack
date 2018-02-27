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


class Lwtnn(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/lwtnn/lwtnn/archive/v1.0.tar.gz"

    version('1.0', 'bb62cd8c1f0a97681206894f7f5a8e95')

    depends_on('boost')
    depends_on('eigen')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)
        spack_env.set('EIGEN_ROOT', self.spec['eigen'].prefix)

    def install(self, spec, prefix):
        make('all')
        install_tree('lib', self.prefix.lib)
        install_tree('bin', self.prefix.bin)
        install_tree('include', self.prefix.include)

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

        fname = 'lwtnn.xml'
        template = Template("""
<tool name="lwtnn" version="${VER}">
  <info url="https://github.com/lwtnn/lwtnn"/>
  <lib name="lwtnn"/>
  <client>
    <environment name="LWTNN_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LWTNN_BASE/lib"/>
    <environment name="INCLUDE" default="$$LWTNN_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$LWTNN_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="eigen"/>
  <use name="boost_system"/>  
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
