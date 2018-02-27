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

class Cascade(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/cascade/cascade-2.2.04-src.tgz"

    version('2.2.04', '01986cfd390c41c6a3e066ff504aa1eb')

    depends_on('lhapdf')
    depends_on('pythia6')

    patch('cascade-2.2.04-drop-dcasrn.patch')

    def install(self, spec, prefix):
       with working_dir(self.version.string):
            configure('--prefix=%s' % prefix,
                      '--enable-static', '--disable-shared', 
                      '--with-pythia6=%s' % spec['pythia6'].prefix,
                      '--with-lhapdf=%s' % spec['lhapdf'].prefix,
                      'LIBS=-lstdc++ -lz','F77=gfortran -fPIC'
                      )
            make()
            make('install')


    @run_after('install')
    def make_merged_lib(self):
        with working_dir(self.prefix.lib):
            ar=which('ar')
            for file in glob.glob('*.a'):
                ar('-x',file)
            args=['rcs', 'libcascade_merged.a']
            for file in glob.glob('*.o'):
                args.append(file)
            ar(*args)
            for file in glob.glob('*.o'):
                os.remove(file)



    def url_for_version(self,version):
        url="http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/cascade/cascade-%s-src.tgz"%version
        return url


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

        fname = 'cascade.xml'
        template = Template("""
<tool name="cascade" version="${VER}">
    <lib name="cascade_merged"/>
  <client>
    <environment name="CASCADE_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CASCADE_BASE/lib"/>
  </client>
  <runtime name="CASCADE_PDFPATH" value="$$CASCADE_BASE/share"/>
  <use name="f77compiler"/>
  <use name="cascade_headers"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'cascade_headers.xml'
        template = Template("""
<tool name="cascade_headers" version="${VER}">
  <client>
    <environment name="CASCADE_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$CASCADE_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

