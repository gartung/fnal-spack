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


class Libtiff(AutotoolsPackage):
    """libtiff graphics format library"""
    homepage = "http://www.simplesystems.org/libtiff/"
    url = "http://download.osgeo.org/libtiff/tiff-4.0.8.tar.gz"

    version('4.0.8', '2a7d1c1318416ddf36d5f6fa4600069b')
    version('4.0.7', '77ae928d2c6b7fb46a21c3a29325157b')
    version('4.0.6', 'd1d2e940dea0b5ad435f21f03d96dd72')
    version('4.0.3', '051c1068e6a0627f461948c365290410')

    depends_on('cmssw.libjpeg-turbo')
    depends_on('zlib')
    depends_on('xz')

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

        fname = 'libtiff.xml'
        template = Template("""<tool name="libtiff" version="$VER">
  <info url="http://www.libtiff.org/"/>
  <lib name="tiff"/>
  <client>
    <environment name="LIBTIFF_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBTIFF_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBTIFF_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="libjpeg-turbo"/>
  <use name="zlib"/>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
