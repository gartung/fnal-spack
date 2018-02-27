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
import os
import re
import glob


class Tbb(Package):
    """Widely used C++ template library for task parallelism.
    Intel Threading Building Blocks (Intel TBB) lets you easily write parallel
    C++ programs that take full advantage of multicore performance, that are
    portable and composable, and that have future-proof scalability.
    """
    homepage = "http://www.threadingbuildingblocks.org/"

    # Only version-specific URL's work for TBB

    version('20161128oss', 'bd71c82574927ce5507abcbcd3be2c1c',
            url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb2017_20161128oss_src.tgz')
    version('20160316oss', '1908b8901730fa1049f0c45d8d0e6d7d',
            url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20160316oss_src.tgz')
    version('20160128oss', '9d8a4cdf43496f1b3f7c473a5248e5cc',
            url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20160128oss_src_0.tgz')
    version('20151115oss', '7fae6a6bbca68bbdc18e844d6721d5e4',
            url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20151115oss_src.tgz')
    version('20150728oss', '2ef1d8cb790324c09aa17360d75dd619',
            url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20150728oss_src.tgz')
    version('20140122oss', '70345f907f5ffe9b2bc3b7ed0d6508bc',
            url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb42_20140122oss_src.tgz')

    def coerce_to_spack(self, tbb_build_subdir):
        for compiler in ["icc", "gcc", "clang"]:
            fs = glob.glob(join_path(tbb_build_subdir, "*.%s.inc" % compiler))
            for f in fs:
                lines = open(f).readlines()
                of = open(f, "w")
                for l in lines:
                    if l.strip().startswith("CPLUS ="):
                        of.write("# coerced to spack\n")
                        of.write("CPLUS = $(CXX)\n")
                    elif l.strip().startswith("CPLUS ="):
                        of.write("# coerced to spack\n")
                        of.write("CONLY = $(CC)\n")
                    else:
                        of.write(l)

    def install(self, spec, prefix):
        #
        # we need to follow TBB's compiler selection logic to get the proper build + link flags
        # but we still need to use spack's compiler wrappers
        # to accomplish this, we do two things:
        #
        # * Look at the spack spec to determine which compiler we should pass to tbb's Makefile
        #
        # * patch tbb's build system to use the compiler wrappers (CC, CXX) for
        #    icc, gcc, clang
        #    (see coerce_to_spack())
        #
        self.coerce_to_spack("build")

        if spec.satisfies('%clang'):
            tbb_compiler = "clang"
        elif spec.satisfies('%intel'):
            tbb_compiler = "icc"
        else:
            tbb_compiler = "gcc"

        mkdirp(prefix)
        mkdirp(prefix.lib)

        #
        # tbb does not have a configure script or make install target
        # we simply call make, and try to put the pieces together
        #
        make("compiler=%s" % (tbb_compiler), "stdver=c++14")

        # install headers to {prefix}/include
        install_tree('include', prefix.include)

        # install libs to {prefix}/lib
        tbb_lib_names = ["libtbb",
                         "libtbbmalloc",
                         "libtbbmalloc_proxy"]

        for lib_name in tbb_lib_names:
            # install release libs
            fs = glob.glob(join_path("build", "*release", lib_name + ".*"))
            for f in fs:
                install(f, prefix.lib)
            # install debug libs if they exist
            fs = glob.glob(join_path("build", "*debug", lib_name + "_debug.*"))
            for f in fs:
                install(f, prefix.lib)

    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        mkdirp(self.spec.prefix.etc + '/scram.d/')
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def write_scram_toolfiles(self):
        from string import Template
        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_GLIBCXX_VER'] = gcc_ver.rstrip().replace('.', '0')
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()
        fname = 'tbb.xml'
        template = Template("""
<tool name="tbb" version="$VER">
  <info url="http://threadingbuildingblocks.org"/>
  <lib name="tbb"/>
  <client>
    <environment name="TBB_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$TBB_BASE/lib"/>
    <environment name="INCLUDE" default="$$TBB_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags CPPDEFINES="TBB_USE_GLIBCXX_VERSION=$GCC_GLIBCXX_VER"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
