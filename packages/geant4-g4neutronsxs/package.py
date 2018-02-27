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
import glob
import os


class Geant4G4neutronsxs(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "http://geant4.web.cern.ch/geant4/support/source/G4NEUTRONXS.1.4.tar.gz"

    version('1.4', '665a12771267e3b31a08c622ba1238a7')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4.web.cern.ch/geant4/support/source/G4NEUTRONXS.%s.tar.gz" % version)

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
        values['PREFIX'] = self.spec.prefix.share + '/data'

        fname = 'geant4data_g4neutronsxs.xml'
        template = Template("""
<tool name="geant4data_g4neutronsxs" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4NEUTRONSXS" default="${PREFIX}"/>
  </client>
  <runtime name="G4NEUTRONXSDATA" value="${PREFIX}/G4NEUTRONXS${VER}" type="path"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
