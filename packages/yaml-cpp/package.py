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


class YamlCpp(CMakePackage):
    """A YAML parser and emitter in C++"""

    homepage = "https://github.com/jbeder/yaml-cpp"
    url = "https://github.com/jbeder/yaml-cpp/archive/release-0.5.1.tar.gz"

    #version('0.5.3', 'e2507c3645fc2bec29ba9a1838fb3951')
    #version('0.5.2', '96bdfa47d38711737d973b23d384d4f2')
    version('0.5.1', '76c47d4a961797092650806dfdfc6cd9')

    depends_on('boost@1.63.0')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DCMAKE_INSTALL_PREFIX:PATH=%s' % prefix,
            '-DBUILD_SHARED_LIBS=YES',
            '-DBoost_NO_SYSTEM_PATHS:BOOL=TRUE',
            '-DBoost_NO_BOOST_CMAKE:BOOL=TRUE',
            '-DBoost_ADDITIONAL_VERSIONS=1.57.0',
            '-DBOOST_ROOT:PATH=%s' % spec['boost'],
            '-DCMAKE_SKIP_RPATH=YES',
            '-DSKIP_INSTALL_FILES=1']
        return options

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

        fname = 'yamlcpp.xml'
        template = Template("""
<tool name="yaml-cpp" version="${VER}">
  <info url="http://code.google.com/p/yaml-cpp/"/>
  <lib name="yaml-cpp"/>
  <client>
    <environment name="YAML_CPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$YAML_CPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$YAML_CPP_BASE/include"/>
  </client>
  <use name="boost"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
