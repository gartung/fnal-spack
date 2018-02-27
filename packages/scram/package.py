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
from glob import glob
from string import Template
import re
import os
import fnmatch
import sys
import shutil


class Scram(Package):
    """SCRAM as used by CMS"""

    homepage = "https://github.com/cms-sw/SCRAM"
    url = "https://github.com/cms-sw/SCRAM/archive/V2_2_6.tar.gz"

    version('2_2_7_pre3', 'b451f27fff6a74f44544d90bd3140ca6')

    depends_on('gmake')

    scram_arch = 'slc_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'

    def install(self, spec, prefix):
        gmake = which('gmake')
        args = ['install']
        args.append('INSTALL_BASE=%s' % prefix)
        args.append('VERSION=V%s' % self.version)
        args.append('PREFIX=%s' % prefix)
        args.append('VERBOSE=1')
        gmake(*args)

        with working_dir(prefix.etc + '/scram.d', create=True):
            gcc = which(spack_f77)
            gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
            gcc_machine = gcc('-dumpmachine', output=str)
            gcc_ver = gcc('-dumpversion', output=str)

            values = {}
            values['GCC_VER'] = gcc_ver.rstrip()
            values['GCC_PREFIX'] = gcc_prefix
            values['GCC_MACHINE'] = gcc_machine.rstrip()

            template = Template("""
  <tool name="gcc-ccompiler" version="${GCC_VER}" type="compiler">
    <client>
      <environment name="GCC_CCOMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags CSHAREDOBJECTFLAGS="-fPIC   "/>
    <flags CFLAGS="-O2 -pthread   "/>
  </tool>
""")
            with open('gcc-ccompiler.xml', 'w') as f:
                f.write(template.substitute(values))
                f.close()

            template = Template("""
  <tool name="gcc-cxxcompiler" version="${GCC_VER}" type="compiler">
    <client>
      <environment name="GCC_CXXCOMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags CPPDEFINES="GNU_GCC _GNU_SOURCE   "/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC   "/>
    <flags CXXFLAGS="-O2 -pthread -pipe -Werror=main -Werror=pointer-arith"/>
    <flags CXXFLAGS="-Werror=overlength-strings -Wno-vla -Werror=overflow   -std=c++1z -ftree-vectorize -Wstrict-overflow -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits -fvisibility-inlines-hidden -fno-math-errno --param vect-max-version-for-alias-checks=50 -Wa,--compress-debug-sections -fno-crossjumping -msse3"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type"/>
    <flags CXXFLAGS="-Wunused -Wparentheses -Wno-deprecated -Werror=return-type"/>
    <flags CXXFLAGS="-Werror=missing-braces -Werror=unused-value"/>
    <flags CXXFLAGS="-Werror=address -Werror=format -Werror=sign-compare"/>
    <flags CXXFLAGS="-Werror=write-strings -Werror=delete-non-virtual-dtor"/>
    <flags CXXFLAGS="-Werror=maybe-uninitialized -Werror=strict-aliasing"/>
    <flags CXXFLAGS="-Werror=narrowing -Werror=uninitialized"/>
    <flags CXXFLAGS="-Werror=unused-but-set-variable -Werror=reorder"/>
    <flags CXXFLAGS="-Werror=unused-variable -Werror=conversion-null"/>
    <flags CXXFLAGS="-Werror=return-local-addr"/>
    <flags CXXFLAGS="-Werror=switch -fdiagnostics-show-option"/>
    <flags CXXFLAGS="-Wno-unused-local-typedefs -Wno-attributes -Wno-psabi"/>
    <flags LDFLAGS="-Wl,-E -Wl,--hash-style=gnu  "/>
    <flags CXXSHAREDFLAGS="-shared -Wl,-E  "/>
    <flags LD_UNIT=" -r -z muldefs "/>
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/lib64" type="path"/>
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$$GCC_CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
""")
            with open('gcc-cxxcompiler.xml', 'w') as f:
                f.write(template.substitute(values))
                f.close()


            template = Template("""
  <tool name="gcc-atomic" version="${GCC_VER}">
    <lib name="atomic"/>
    <client>
      <environment name="GCC_ATOMIC_BASE" default="${GCC_PREFIX}"/>
    </client>
  </tool>
""")

            with open('gcc-cxxcompiler.xml', 'w') as f:
                f.write(template.substitute(values))
                f.close()
            template = Template("""
  <tool name="gcc-f77compiler" version="${GCC_VER}" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="GCC_F77COMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2 -cpp"/>
    <flags LDFLAGS="-L$$(GCC_F77COMPILER_BASE)/lib64"/>
    <flags LDFLAGS="-L$$(GCC_F77COMPILER_BASE)/lib"/>
    <flags FOPTIMISEDFLAGS="-O2   "/>
    <flags FSHAREDOBJECTFLAGS="-fPIC   "/>
  </tool>
""")
            with open('gcc-f77compiler.xml', 'w') as f:
                f.write(template.substitute(values))
                f.close()

            template = Template("""
<tool name="root_cxxdefaults" version="6">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="${GCC_PREFIX}" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="${GCC_PREFIX}/include/c++/${GCC_VER}" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="${GCC_PREFIX}/include/c++/${GCC_VER}/${GCC_MACHINE}" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="${GCC_PREFIX}/include/c++/${GCC_VER}/backward" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include" type="path"/>
</tool>
""")
            with open('root_cxxdefaults.xml', 'w') as f:
                f.write(template.substitute(values))
                f.close()

            contents = """
  <tool name="sockets" version="1.0">
    <lib name="nsl"/>
    <lib name="crypt"/>
    <lib name="dl"/>
    <lib name="rt"/>
  </tool>
"""
            if sys.platform == 'darwin':
                contents = """
  <tool name="sockets" version="1.0">
    <lib name="dl"/>
  </tool>
"""
            with open('sockets.xml', 'w') as f:
                f.write(contents)
                f.close()
            contents = """
  <tool name="opengl" version="XFree4.2">
    <lib name="GL"/>
    <lib name="GLU"/>
    <use name="x11"/>
    <environment name="ORACLE_ADMINDIR" default="/etc"/>
"""
            if sys.platform == 'darwin':
                contents += """
    <client>
      <environment name="OPENGL_BASE" default="/System/Library/Frameworks/OpenGL.framework/Versions/A"/>
      <environment name="INCLUDE"     default="$OPENGL_BASE/Headers"/>
      <environment name="LIBDIR"      default="$OPENGL_BASE/Libraries"/>
    </client>
"""
            contents += """</tool>"""
            with open('opengl.xml', 'w') as f:
                f.write(contents)
                f.close()

            contents = """
  <tool name="x11" version="R6">
    <use name="sockets"/>
  </tool>
"""
            with open('x11.xml', 'w') as f:
                f.write(contents)
                f.close()

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('SCRAM_ARCH', self.scram_arch)
