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


class FrontierClient(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/frontier_client/2.8.20/frontier_client__2.8.20__src.tar.gz"

    version('2.8.20', 'e2ea893b02eab539a0cf6a3812f4937c')

    patch('frontier_client-2.8.20-add-python-dbapi.patch')

    depends_on('openssl')
    depends_on('expat')
    depends_on('zlib')
    depends_on('pacparser')
    depends_on('python')

    def build(self, spec, prefix):
        make('-j1', 'EXPAT_DIR=%s' % spec['expat'].prefix,
             'PACPARSER_DIR=%s' % spec['pacparser'].prefix,
             'COMPILER_TAG=gcc_%s' % spec.compiler.version,
             'ZLIB_DIR=%s' % spec['zlib'].prefix,
             'OPENSSL_DIR=%s' % spec['openssl'].prefix,
             'CXXFLAGS=-ldl', 'CFLAGS=-I%s' % spec['openssl'].prefix.include,
             'all'
             )

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        make('-j1', 'EXPAT_DIR=%s' % spec['expat'].prefix,
             'PACPARSER_DIR=%s' % spec['pacparser'].prefix,
             'COMPILER_TAG=gcc_%s' % spec.compiler.version,
             'ZLIB_DIR=%s' % spec['zlib'].prefix,
             'OPENSSL_DIR=%s' % spec['openssl'].prefix,
             'CXXFLAGS=-ldl',
             'distdir=%s' % prefix,
             'dist'
             )
        install_tree('python', prefix + '/python')

    def url_for_version(self, version):
        """Handle version string."""
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/frontier_client/%s/frontier_client__%s__src.tar.gz" % (version, version)

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

        fname = 'frontier_client.xml'
        template = Template("""<tool name="frontier_client" version="$VER">
  <lib name="frontier_client"/>
  <client>
    <environment name="FRONTIER_CLIENT_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$FRONTIER_CLIENT_BASE/include"/>
    <environment name="LIBDIR" default="$$FRONTIER_CLIENT_BASE/lib"/>
  </client>
  <runtime name="FRONTIER_CLIENT" value="$$FRONTIER_CLIENT_BASE/"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="openssl"/>
  <use name="expat"/>
  <runtime name="PYTHONPATH" value="$$FRONTIER_CLIENT_BASE/python/lib" type="path"/>
  <use name="python"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
