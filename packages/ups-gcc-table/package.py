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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ups-gcc-table
#
# You can edit this file again by typing:
#
#     spack edit ups-gcc-table
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import re


class UpsGccTable(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://cdcvs.fnal.gov/projects/build-framework-gcc-ssi-build"
    url = "http://cdcvs.fnal.gov/projects/build-framework-gcc-ssi-build"

    version(
        'v6_3_0',
        git='http://cdcvs.fnal.gov/projects/build-framework-gcc-ssi-build',
        tag='v6_3_0')

    depends_on('ups')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        ups = which('ups')
        cp = which('cp')
        flvr = ups('flavor', output=str)
        cp('-rpv', '%s/ups' % self.stage.source_path, '%s' % prefix)
        perl = which('perl')
        perl(
            '-p',
            '-i~',
            '-e',
            's|\$\{UPS_PROD_FLAVOR\}||',
            '%s/ups/gcc.table' %
            prefix)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.cc).rstrip()
        print gcc_prefix
        ups('declare', 'gcc', '%s' %
            spec.version, '-r', gcc_prefix, '-f', flvr, '-m', '%s/ups/gcc.table' %
            prefix, '-z', '%s/../products' %
            prefix)
