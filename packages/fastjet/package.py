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


class Fastjet(AutotoolsPackage):
    """Fastjet"""

    homepage = "http://fastjet.fr/"
    url = "https://github.com/cms-externals/fastjet"

    version('3.1.0', git='https://github.com/cms-externals/fastjet', branch='cms/v3.1.0')

    def configure_args(self):
        args = [
            '--enable-shared',
            '--enable-atlascone',
            '--enable-cmsiterativecone',
            '--enable-siscone',
            '--enable-allcxxplugins'
        ]
        if 'CXXFLAGS' in env and env['CXXFLAGS']:
            env['CXXFLAGS'] += ' ' + \
                '-O3 -Wall -ffast-math -ftree-vectorize -msse3'
        else:
            env['CXXFLAGS'] = '-O3 -Wall -ffast-math -ftree-vectorize -msse3'
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

        fname = 'fastjet.xml'
        template = Template("""<tool name="fastjet" version="$VER">
    <info url="http://www.lpthe.jussieu.fr/~salam/fastjet/"/>
    <lib name="fastjetplugins"/>
    <lib name="fastjettools"/>
    <lib name="siscone"/>
    <lib name="siscone_spherical"/>
    <lib name="fastjet"/>
    <client>
      <environment name="FASTJET_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$FASTJET_BASE/lib"/>
      <environment name="INCLUDE" default="$$FASTJET_BASE/include"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
