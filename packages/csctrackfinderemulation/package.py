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
import distutils.dir_util as du

class Csctrackfinderemulation(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('1.2', git='https://github.com/cms-externals/CSCTrackFinderEmulation', branch='cms/CMSSW_8_1_X')


    def install(self, spec, prefix):
        make()
        make('install')
        du.copy_tree('installDir',prefix)

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

        fname = 'csctrackfinderemulation.xml'
        template = Template("""
<tool name="CSCTrackFinderEmulation" version="${VER}">
  <lib name="CSCTrackFinderEmulation"/>
  <client>
    <environment name="CSCTRACKFINDEREMULATION_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CSCTRACKFINDEREMULATION_BASE/lib64"/>
    <environment name="INCLUDE" default="$$CSCTRACKFINDEREMULATION_BASE/include"/>
  </client>
  <runtime name="CSC_TRACK_FINDER_DATA_DIR" default="$$CSCTRACKFINDEREMULATION_BASE/data/"/>
  <runtime name="CMSSW_SEARCH_PATH" default="$$CSCTRACKFINDEREMULATION_BASE/data" type="path"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
