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


class Libxml2(AutotoolsPackage):
    """Libxml2 is the XML C parser and toolkit developed for the Gnome
       project (but usable outside of the Gnome platform), it is free
       software available under the MIT License."""
    homepage = "http://xmlsoft.org"
    url = "http://xmlsoft.org/sources/libxml2-2.9.2.tar.gz"

    version('2.9.4', 'ae249165c173b1ff386ee8ad676815f5')
    version('2.9.2', '9e6a9aca9d155737868b3dc5fd82f788')
    version('2.7.8', '8127a65e8c3b08856093099b52599c86')

    variant('python', default=True, description='Enable Python support')

    depends_on('python')
    depends_on('zlib')
    depends_on('xz')

    depends_on('pkg-config@0.9.0:', type='build')

    def configure_args(self):
        spec = self.spec

        args = ["--with-lzma=%s" % spec['xz'].prefix]

        if '+python' in spec:
            args.extend([
                '--with-python={0}'.format(spec['python'].home),
                '--with-python-install-dir={0}'.format(site_packages_dir)
            ])
        else:
            args.append('--without-python')

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

        fname = 'libxml2.xml'
        template = """<tool name="libxml2" version="$VER">
  <info url="http://xmlsoft.org/"/>
  <lib name="xml2"/>
  <client>
    <environment name="LIBXML2_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBXML2_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBXML2_BASE/include/libxml2"/>
  </client>
  <runtime name="PATH" value="$$LIBXML2_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
"""
        contents = Template(template).substitute(values)
        self.write_scram_toolfile(contents, fname)
