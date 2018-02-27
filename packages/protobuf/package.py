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
import spack.util.web


class Protobuf(AutotoolsPackage):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url = "https://github.com/google/protobuf/archive/v3.2.0.tar.gz"
    root_cmakelists_dir = "cmake"

    version('3.4.0', '1d077a7d4db3d75681f5c333f2de9b1a')
    version('3.3.0', 'f0f712e98de3db0c65c0c417f5e7aca8')
    version('3.2.0', 'efaa08ae635664fb5e7f31421a41a995', preferred=True)
    version('3.1.0', '39d6a4fa549c0cce164aa3064b1492dc')
    version('3.0.2', '7349a7f43433d72c6d805c6ca22b7eeb')
    # does not build with CMake:
    # version('2.5.0', '9c21577a03adc1879aba5b52d06e25cf')

    depends_on('zlib')
    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build') 
    depends_on('libtool', type='build')

    conflicts('%gcc@:4.6')  # Requires c++11


    def configure_args(self):
        args = [
            '--disable-static',
            '--disable-dependency-tracking',
            'CXXFLAGS=-I%s' % self.spec['zlib'].prefix.include,
            'CFLAGS=-I%s' % self.spec['zlib'].prefix.include,
            'LDFLAGS=-L%s' % self.spec['zlib'].prefix.lib
        ]
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

        fname = 'protobuf.xml'
        template = Template("""
<tool name="protobuf" version="${VER}">
  <lib name="protobuf"/>
  <client>
    <environment name="PROTOBUF_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PROTOBUF_BASE/include"/>
    <environment name="LIBDIR" default="$$PROTOBUF_BASE/lib"/>
    <environment name="BINDIR" default="$$PROTOBUF_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$$PROTOBUF_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
