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
import shutil
from datetime import date



class Castor(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/2.1.13-*/2.1.13-9/castor-2.1.13-9.tar.gz"


    version('2.1.13-9', '44084334e0ec70f71b5d366dcd70c959')
    #version('2.1.16-13', '5a2cf6992ac4c1a2dcf7eb90e14233e5')
    #version('2.1.16-18', '51ed4ad6c76c9f7ecd9bbaae6fbc57ba')

    depends_on('uuid-cms')

    patch('castor-2.1.13.6-fix-memset-in-showqueues.patch')
    patch('castor-2.1.13.9-fix-link-libuuid.patch')


    def patch(self):
        filter_file('-Werror','-Werror -Wno-error=unused-but-set-variable','config/Imake.tmpl')
        filter_file('--no-undefined', '', 'config/Imake.rules')
        perl=which('perl')
        perl('-pi', '-e', 's/\ \ __MAJORVERSION__/%s/'%self.version[0], 'h/patchlevel.h')
        perl('-pi', '-e', 's/\ \ __MINORVERSION__/%s/'%self.version[1], 'h/patchlevel.h')
        perl('-pi', '-e', 's/\ \ __MAJORRELEASE__/%s/'%self.version[2], 'h/patchlevel.h')
        perl('-pi', '-e', 's/\ \ __MINORRELEASE__/%s/'%self.version[3], 'h/patchlevel.h')
        perl('-p', '-i', '-e', 's!__PATCHLEVEL__!%s!;s!__BASEVERSION__!\"%s\"!;s!__TIMESTAMP__!%s!'
             %(self.version.up_to(-1),self.version.up_to(3),date.today().isoformat()),' h/patchlevel.h')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('CASTOR_NOSTK','yes')
        spack_env.append_flags('LDFLAGS', '-L%s' % self.spec['uuid-cms'].prefix.lib)
        spack_env.append_flags('CXXFLAGS', '-I%s' % self.spec['uuid-cms'].prefix.include)

    def install(self, spec, prefix):
        configure()
        make('client')
        make('installclient'
                ,'MAJOR_CASTOR_VERSION=%s' % self.version.dotted.up_to(2)
                ,'MINOR_CASTOR_VERSION=%s' % self.version.dotted.up_to(-2)
                ,'EXPORTLIB=/'
                ,'DESTDIR=%s'%prefix
                ,'PREFIX= '
                ,'CONFIGDIR=etc'
                ,'FILMANDIR=usr/share/man/man4'
                ,'LIBMANDIR=usr/share/man/man3'
                ,'MANDIR=usr/share/man/man1'
                ,'LIBDIR=lib'
                ,'BINDIR=bin'
                ,'LIB=lib'
                ,'BIN=bin'
                ,'DESTDIRCASTOR=include/shift'
                ,'TOPINCLUDE=include'
                 )
        shutil.move(prefix.usr.bin, prefix.bin)


    def url_for_version(self, version):
        url = "http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/%s-*/%s/castor-%s.tar.gz" % (version.up_to(3), version.string, version.string)
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
        import sys
        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'castor_header.xml'
        template = Template("""
<tool name="castor_header" version="${VER}">
  <client>
    <environment name="CASTOR_HEADER_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$CASTOR_HEADER_BASE/include"/>
    <environment name="INCLUDE" default="$$CASTOR_HEADER_BASE/include/shift"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$CASTOR_HEADER_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$CASTOR_HEADER_BASE/include/shift" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'castor.xml'
        template = Template("""
<tool name="castor" version="${VER}">
  <lib name="shift"/>
  <lib name="castorrfio"/>
  <lib name="castorclient"/>
  <lib name="castorcommon"/>
  <client>
    <environment name="CASTOR_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CASTOR_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$CASTOR_BASE/bin" type="path"/>
  <use name="castor_header"/>
  <use name="libuuid"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
