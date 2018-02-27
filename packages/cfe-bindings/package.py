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


class CfeBindings(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://releases.llvm.org/5.0.0/cfe-5.0.0.src.tar.xz"

    version('5.0.0', '699c448c6d6d0edb693c87beb1cc8c6e')
    version('4.0.1', 'a6c7b3e953f8b93e252af5917df7db97')

    extends('python')

    depends_on('llvm@5.0.0~gold+python+shared_libs',
               type='build', when='@5.0.0')
    depends_on('llvm@4.0.1~gold+python+shared_libs',
               type='build', when='@4.0.1')


    def install(self, spec, prefix):
        install_tree('%s/bindings/python/clang/' %
                     self.stage.source_path,
                     self.prefix.lib + '/python2.7/site-packages/clang')
        install('%s/libclang.so' % self.spec['llvm'].prefix.lib,
                '%s/libclang.so' % self.prefix.lib)


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LLVM_BASE', self.prefix)


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
        import re

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))
        pyvers = str(self.spec['python'].version).split('.')
        pyver = pyvers[0] + '.' + pyvers[1]

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['LIB'] = self.spec.prefix.lib
        values['PYVER'] = pyver

        fname = 'pyclang.xml'
        template = Template("""<tool name="pyclang" version="${VER}">
  <client>
    <environment name="PYCLANG_BASE" default="${PFX}"/>
  </client>
  <runtime name="PYTHONPATH" value="${LIB}/python${PYVER}/site-packages" type="path"/>
  <use name="python"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
