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


class Photospp(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos++/photos++-3.61-src.tgz"

    version('3.61', 'b5519bb2b22a51710f67014704f6795a')

    # FIXME: Add dependencies if required.
    depends_on('hepmc')

    def install(self, spec, prefix):
        with working_dir(str(spec.version)):
            configure('--prefix=%s' % prefix, '--with-hepmc=%s' %
                      spec['hepmc'].prefix)
            make()
            make('install')

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

        fname = 'photospp.xml'
        template = Template("""
<tool name="photospp" version="${VER}">
  <lib name="Photospp"/>
  <lib name="PhotosppHepMC"/>
  <lib name="PhotosppHEPEVT"/>
  <client>
    <environment name="PHOTOSPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PHOTOSPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$PHOTOSPP_BASE/include"/>
  </client>
  <use name="hepmc"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
