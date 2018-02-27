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


class Hepmc(Package):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "http://hepmc.web.cern.ch/hepmc/"
    url = "http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.09.tar.gz"

    version('2.06.09', 'c47627ced4255b40e731b8666848b087')
    version('2.06.08', 'a2e889114cafc4f60742029d69abd907')
    version('2.06.07', '11d7035dccb0650b331f51520c6172e7')

    depends_on("cmake", type='build')

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        options = [source_directory]
        options.append('-Dmomentum:STRING=GEV')
        options.append('-Dlength:STRING=MM')
        options.extend(std_cmake_args)

        with working_dir(build_directory, create=True):
            cmake(*options)
            make()
            make('install')
            fix_darwin_install_name(prefix.lib)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)

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

        fname = 'hepmc.xml'
        template = Template("""<tool name="HepMC" version="$VER">
  <lib name="HepMCfio"/>
  <lib name="HepMC"/>
  <client>
    <environment name="HEPMC_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$HEPMC_BASE/lib"/>
  </client>
  <use name="hepmc_headers"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$HEPMC_BASE/include" type="path"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'hepmc_headers.xml'
        template = Template("""<tool name="hepmc_headers" version="$VER">
  <client>
    <environment name="HEPMC_HEADERS_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$HEPMC_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
