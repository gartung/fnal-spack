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


class Yoda(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://cern.ch/service-spi/external/MCGenerators/distribution/yoda/yoda-1.6.5-src.tgz"

    version('1.6.5', '634fa27412730e511ca3d4c67f6086e7')

    # FIXME: Add dependencies if required.
    depends_on('root')
    depends_on('python')
    depends_on('py-cython', type='build')

    def install(self, spec, prefix):
        with working_dir(str(self.spec.version), create=False):
            configure('--enable-root', '--prefix=%s' % self.prefix)
            make('all')
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

        fname = 'yoda.xml'
        template = Template("""
<tool name="yoda" version="${VER}">
  <lib name="YODA"/>
  <client>
    <environment name="YODA_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$YODA_BASE/lib"/>
    <environment name="INCLUDE" default="$$YODA_BASE/include"/>
  </client>
  <use name="root_cxxdefaults"/>
  <runtime name="PYTHONPATH" value="$$YODA_BASE/lib/python2.7/site-packages" type="path"/>
  <runtime name="PATH"       value="$$YODA_BASE/bin" type="path"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
