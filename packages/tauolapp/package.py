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
import os
import glob 

class Tauolapp(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-1.1.5-src.tgz"

    # FIXME: Add proper versions and checksums here.
    version('1.1.5', '2d9a3bc7536ddc5d937bbe711ddbadbe')

    # FIXME: Add dependencies if required.
    depends_on('hepmc')
    depends_on('pythia8')
    depends_on('lhapdf')
    depends_on('boost')

    def patch(self):
        with working_dir(str(self.version)):
            if os.path.exists('./config/config.sub'):
                os.remove('./config/config.sub')
                install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
            if os.path.exists('./config/config.guess'):
                os.remove('./config/config.guess')
                install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')


    def setup_environment(self, spack_env, run_env):
        self.HEPMC_ROOT = self.spec['hepmc'].prefix
        self.HEPMC_VERSION = self.spec['hepmc'].version
        self.LHAPDF_ROOT = self.spec['lhapdf'].prefix
        self.PYTHIA8_ROOT = self.spec['pythia8'].prefix
        spack_env.set('HEPMCLOCATION',self.HEPMC_ROOT)
        spack_env.set('HEPMCVERSION',self.HEPMC_VERSION)
        spack_env.set('LHAPDF_LOCATION',self.LHAPDF_ROOT)
        spack_env.set('PYTHIA8_LOCATION',self.PYTHIA8_ROOT)


    def install(self, spec, prefix):
        with working_dir(str(self.version)):
            configure('--prefix=%s' % prefix,
                      '--with-hepmc=%s' % self.HEPMC_ROOT,
                      '--with-pythia8=%s' % self.PYTHIA8_ROOT,
                      '--with-lhapdf=%s' % self.LHAPDF_ROOT,
                      'CPPFLAGS=-I%s/include' % self.spec['boost'].prefix)
            make()
            make('install')
            mkdirp(prefix.share)
            with working_dir(join_path(self.stage.source_path, str(self.version), 
                    'TauSpinner/examples/CP-tests/Z-pi')):
                for f in glob.glob('*.txt'):    
                    install(f, join_path(prefix.share, f))

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

        fname = 'tauolapp.xml'
        template = Template("""
<tool name="tauolapp" version="${VER}">
  <lib name="TauolaCxxInterface"/>
  <lib name="TauolaFortran"/>
  <lib name="TauolaTauSpinner"/>
  <client>
    <environment name="TAUOLAPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TAUOLAPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$TAUOLAPP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="hepmc"/>
  <use name="f77compiler"/>
  <use name="pythia8"/>
  <use name="lhapdf"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
