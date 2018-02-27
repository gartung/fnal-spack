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


class Xrootd(CMakePackage):
    """The XROOTD project aims at giving high performance, scalable fault
       tolerant access to data repositories of many kinds."""
    homepage = "http://xrootd.org"
    url = "http://xrootd.org/download/v4.6.0/xrootd-4.6.0.tar.gz"

    version('4.6.0', '5d60aade2d995b68fe0c46896bc4a5d1')
    version('4.5.0', 'd485df3d4a991e1c35efa4bf9ef663d7')
    version('4.4.1', '72b0842f802ccc94dede4ac5ab2a589e')
    version('4.4.0', '58f55e56801d3661d753ff5fd33dbcc9')
    version('4.3.0', '39c2fab9f632f35e12ff607ccaf9e16c')

    depends_on('cmake@2.6:', type='build')
    depends_on('python')

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
        pyvers = str(self.spec['python'].version).split('.')
        pyver = pyvers[0] + '.' + pyvers[1]

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['PYVER'] = pyver

        fname = 'xrootd.xml'
        template = Template("""<tool name="xrootd" version="$VER">
  <lib name="XrdUtils"/>
  <lib name="XrdClient"/>
  <client>
    <environment name="XROOTD_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$XROOTD_BASE/include/xrootd"/>
    <environment name="INCLUDE" default="$$XROOTD_BASE/include/xrootd/private"/>
    <environment name="LIBDIR" default="$$XROOTD_BASE/lib64"/>
  </client>
  <runtime name="PATH" value="$$XROOTD_BASE/bin" type="path"/>
  <runtime name="PYTHONPATH" value="$$XROOTD_BASE/lib/python${PYVER}/site-packages" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
