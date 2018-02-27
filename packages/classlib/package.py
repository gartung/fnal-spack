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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install classlib
#
# You can edit this file again by typing:
#
#     spack edit classlib
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Classlib(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/classlib/3.1.3/classlib-3.1.3.tar.bz2"

    version('3.1.3', '9114995676f4378e56ebacdd21220598')

    patch('classlib-3.1.3-fix-gcc47-cxx11.patch')
    patch('classlib-3.1.3-fix-obsolete-CLK_TCK.patch')
    patch('classlib-3.1.3-fix-unwind-x86_64.patch')
    patch('classlib-3.1.3-gcc46.patch')
    patch('classlib-3.1.3-memset-fix.patch')
    patch('classlib-3.1.3-sl6.patch')

    # FIXME: Add dependencies if required.
    depends_on('bzip2')
    depends_on('pcre')
    depends_on('xz')
    depends_on('openssl')
    depends_on('zlib')

    def configure_args(self):
        args = ['--with-zlib-includes=%s' % self.spec['zlib'].prefix.include,
                '--with-zlib-libraries=%s' % self.spec['zlib'].prefix.lib,
                '--with-bz2lib-includes=%s' % self.spec['bzip2'].prefix.include,
                '--with-bz2lib-libraries=%s' % self.spec['bzip2'].prefix.lib,
                '--with-pcre-includes=%s' % self.spec['pcre'].prefix.include,
                '--with-pcre-libraries=%s' % self.spec['pcre'].prefix.lib,
                '--with-openssl-includes=%s' % self.spec['openssl'].prefix.include,
                '--with-openssl-libraries=%s' % self.spec['openssl'].prefix.lib,
                '--with-lzma-includes=%s' % self.spec['xz'].prefix.include,
                '--with-lzma-libraries=%s' % self.spec['xz'].prefix.lib]
        return args

    @run_before('build')
    def patch_makefile(self):
        perl = which('perl')
        perl('-p', '-i', '-e',
             's{-llzo2}{}g;!/^\S+: / ' +
             '&& s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g',
             'Makefile')

    def build(self, spec, prefix):
        make('CXXFLAGS=-Wno-error -ansi -pedantic -W -Wall -Wno-long-long ')

    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):

        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'classlib.xml'

        template = Template("""<tool name="classlib" version="$VER">
    <info url="http://cmsmac01.cern.ch/~lat/exports/"/>
    <client>
      <environment name="CLASSLIB_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$CLASSLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$CLASSLIB_BASE/include"/>
      <flags CPPDEFINES="__STDC_LIMIT_MACROS"/>
      <flags CPPDEFINES="__STDC_FORMAT_MACROS"/>
      <lib name="classlib"/>
      <use name="zlib"/>
      <use name="bz2lib"/>
      <use name="pcre"/>
      <use name="openssl"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
