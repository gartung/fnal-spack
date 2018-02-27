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


class Giflib(AutotoolsPackage):
    """The GIFLIB project maintains the giflib service library, which has
    been pulling images out of GIFs since 1989."""

    homepage = "http://giflib.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/giflib/giflib-5.1.4.tar.bz2"

    version('5.1.4', '2c171ced93c0e83bb09e6ccad8e3ba2b')

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

        fname = 'giflib.xml'
        template = Template("""<tool name="giflib" version="$VER">
    <info url="http://giflib.sourceforge.net"/>
    <lib name="gif"/>
    <client>
      <environment name="GIFLIB_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$GIFLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$GIFLIB_BASE/include"/>
    </client>
    <runtime name="PATH" value="$$GIFLIB_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
