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
from glob import glob


class FireworksGeometry(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "https://github.com/cms-data/Fireworks-Geometry/archive/V07-05-01.tar.gz"

    version('07.05.01', '9f40fdf89286392d1d39d5ed52981051')
    version('07.05.02', '0277dd37c0ff7664ea733445445efb6a')
    version('07.05.03', 'cea2d9a9c03cb95470552f7fd73d3537')


    def install(self, spec, prefix):
        matches = []
        instpath = prefix.share+'/data/'
        mkdirp(instpath)
        for m in glob('*.root'):
            install(m, join_path(instpath, m))

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        return "https://github.com/cms-data/Fireworks-Geometry/archive/V%s.tar.gz" % version.dashed

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
        values['PFX'] = self.spec.prefix.share + '/data'

        fname = 'fireworks-geometry.xml'
        template = Template("""
<tool name="fwlitedata" version="${VER}">
  <client>
    <environment name="CMSSWDATA_BASE" default="${PFX}"/>
    <environment name="CMSSW_DATA_PATH" default="$$CMSSWDATA_BASE"/>
  </client>
  <runtime name="CMSSW_DATA_PATH" value="$$CMSSWDATA_BASE" handler="warn" type="path"/>
  <runtime name="CMSSW_SEARCH_PATH" default="${PFX}" handler="warn" type="path"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
