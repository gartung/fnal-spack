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


class UpsMysqlClientTable(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version(
        'v5_5_54',
        git='http://cdcvs.fnal.gov/projects/build-framework-mysql-client-ssi-build',
        tag='v5_5_54')

    # FIXME: Add dependencies if required.
    depends_on('ups')
    depends_on('mysql')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        ups = which('ups')
        flvr = ups('flavor', output=str).strip('\n')
        print flvr
        cp = which('cp')
        cp('-rpv', '%s/ups' % self.stage.source_path, '%s' % prefix)
        perl = which('perl')
        perl(
            '-p',
            '-i~',
            '-e',
            's|\$\{MYSQL_CLIENT_FQ_DIR\}|%s|'%spec['mysql'].prefix,
            '%s/ups/mysql_client.table' %
            prefix)
        ups(
            'declare',
            'mysqlclient',
            '%s' %
            spec.version,
            '-r',
            '%s' %
            spec['mysql'].prefix,
            '-f',
            flvr,
            '-q','e14',
            '-m',
            '%s/ups/mysql_client.table' %
            prefix,
            '-z',
            '%s/../products' %
            prefix)
