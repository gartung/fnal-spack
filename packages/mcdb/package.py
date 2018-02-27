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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mcdb
#
# You can edit this file again by typing:
#
#     spack edit mcdb
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Mcdb(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://mcdb.cern.ch/distribution/api/mcdb-api-1.0.3.tar.gz"

    version('1.0.3', '587a2699d3240561ccaf479c8edcfdeb')
    version('1.0.2', 'f8c5cba0b66c7241115bc74e846c7814')
    version('1.0.1', 'c93bafcfc129a875ce5097c4e5fcf16e')

    # FIXME: Add dependencies if required.
    depends_on('xerces-c')

    def install(self, spec, prefix):
        contents = """
PLATFORM = slc_amd64_gcc
CC       = gcc
CXX      = g++
CFLAGS   = -O2 -pipe -Wall -W -fPIC
CXXFLAGS = -O2 -pipe -Wall -W -fPIC
LINK     = g++
LFLAGS   = -shared -Wl,-soname,libmcdb.so
XERCESC  = %s
""" % spec['xerces-c'].prefix
        with open('config.mk', 'w') as f:
            f.write(contents)
            f.close()
        make()
        install_tree('lib', prefix + '/lib')
        install_tree('interface', prefix + '/interface')

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

        fname = 'mcdb.xml'
        template = Template("""
<tool name="mcdb" version="$VER">
  <lib name="mcdb"/>
  <client>
    <environment name="MCDB_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$MCDB_BASE/lib"/>
    <environment name="INCLUDE" default="$$MCDB_BASE/interface"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="xerces-c"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
