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
#     spack install ups
#
# You can edit this file again by typing:
#
#     spack edit ups
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Ups(Package):

    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    #homepage = "http://www.example.com"
    url      = "http://home.fnal.gov/~gartung/ups-5.2.0-source.tar.bz2"

    version('5.2.0', '2a48103033661ff84359cb02fec09420')


    def install(self, spec, prefix):
        make('all', 'UPS_DIR=%s'%self.stage.source_path, 'PRODUCTS=%s'%self.prefix)
        rsync=which('rsync')
        rsync('-av','--exclude=*.o','%s/ups/' % self.stage.path,'%s/' % self.prefix)
        flvr='NULL'
        mkdirp('%s/../../../products/.upsfiles'%self.prefix)
        mkdirp('%s/../../../products/.updfiles'%self.prefix)
        f=open('%s/../../../products/.upsfiles/dbconfig'%self.prefix,'w+')
        contents="""
FILE = DBCONFIG
AUTHORIZED_NODES = *
VERSION_SUBDIR = 1
PROD_DIR_PREFIX = ${UPS_THIS_DB}
UPD_USERCODE_DIR = ${UPS_THIS_DB}/.updfiles
"""
        f.write(contents)
        f.close()
        f=open('%s/../../../products/.updfiles/updusr.pm'%self.prefix,'w+')
        f.write("require 'default_updusr.pm';")
        f.close()
        f=open('%s/../../../products/.updfiles/updconfig'%self.prefix,'w+')
        contents="""
File = updconfig

GROUP:
  product       = ANY
  flavor        = ANY
  qualifiers    = ANY
  options       = ANY
  dist_database = ANY
  dist_node     = ANY

COMMON:
     UPS_THIS_DB = \"${UPD_USERCODE_DB}\"

     UPS_PROD_DIR = \"${UPS_PROD_NAME}/${UPS_PROD_VERSION}/${DASH_PROD_FLAVOR}${DASH_PROD_QUALIFIERS}\"



  UNWIND_PROD_DIR = \"${PROD_DIR_PREFIX}/${UPS_PROD_DIR}\"


      UPS_UPS_DIR = \"ups\"

   UNWIND_UPS_DIR = \"${UNWIND_PROD_DIR}/${UPS_UPS_DIR}\"

 UPS_TABLE_FILE  = \"${UPS_PROD_NAME}.table\"
UNWIND_TABLE_DIR = \"${UNWIND_UPS_DIR}\"



END:
"""
        f.write(contents)
        f.close()
        f=open('%s/../../../products/setups_layout'%self.prefix,'w+')
        f.write('s_setenv UPS_THIS_DB $SETUPS_DIR\n')
        f.write('s_setenv PROD_DIR_PREFIX $SETUPS_DIR\n')
        f.close()

        ups=which('%s/bin/ups'%self.prefix)
        flavor=ups('flavor',output=str)
        flvr=flavor.strip('\n')
#        ups('declare','ups','v5_2_0','-f',flvr,'-r','%s'%self.prefix,'-4','-m','%s/ups/ups.table'%self.prefix,'-C','-z','%s/../../../products'%self.prefix)
#        ups('declare','ups','v5_2_0','-C','-c','-z','%s/../../../products'%self.prefix)
        cp=which('cp')
        cp('-p','%s/ups/setups'%self.prefix,'%s/../../../products/setups'%self.prefix)
        cp('-p','%s/ups/setup'%self.prefix,'%s/../../../products/setup'%self.prefix)
        
    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('UPS_DIR', self.prefix)
        run_env.set('UPS_SHELL', '/bin/bash')
        run_env.set('PRODUCTS', '%s/../../../products' % self.prefix)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('UPS_DIR', self.prefix)
        run_env.set('UPS_SHELL', 'sh')
        run_env.set('PRODUCTS', '%s/../../../products' % self.prefix)

