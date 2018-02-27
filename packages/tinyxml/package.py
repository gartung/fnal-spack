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
import sys


class Tinyxml(Package):
    """FIXME: Put a proper description of your package here."""
    homepage = "https://github.com/cms-externals/tinyxml"
    url = "http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/tinyxml/2.5.3-giojec/tinyxml.2.5.3-3b1ed8542a820e77de84bc08734bde904c3b12be.tgz"

    version('2.5.3', '3126b4a2dbfbd087e28faca4ad62cd31',
            url='http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/tinyxml/2.5.3-giojec/tinyxml.2.5.3-3b1ed8542a820e77de84bc08734bde904c3b12be.tgz')
    if sys.platform == 'darwin':
        patch('tinyxml.patch')

    depends_on('boost@1.63.0+python^python+shared')
    depends_on('gmake', type='build')

    def install(self, spec, prefix):
        gmake = which('gmake')
        gmake('BOOST_ROOT=%s' % spec['boost'].prefix)
        cp = which('cp')
        md = which('mkdir')
        md('%s' % self.prefix.lib)
        md('%s' % self.prefix.include)
        if sys.platform == 'darwin':
            cp('-v', 'libtinyxml.dylib', prefix.lib)
            fix_darwin_install_name(prefix.lib)
        else:
            cp('-v', 'libtinyxml.so', prefix.lib)
        cp('-v', 'tinystr.h', 'tinyxml.h', prefix.include)

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

        fname = 'tinyxml.xml'
        template = Template("""<tool name="tinyxml" version="$VER">
  <info url="https://sourceforge.net/projects/tinyxml/"/>
   <lib name="tinyxml"/>
  <client>
    <environment name="TINYXML_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$TINYXML_BASE/lib"/>
    <environment name="INCLUDE" default="$$TINYXML_BASE/include"/>
  </client>  
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
