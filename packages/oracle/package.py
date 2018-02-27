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
import glob
import shutil
import os


class Oracle(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-basic-linux.x64-12.1.0.2.0.zip"

    version('12.1.0.2.0', 'd5ef30bc0506e0b0dae4dc20c76b8dbe')
    resource(name='basiclite', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-basiclite-linux.x64-12.1.0.2.0.zip',
             md5='3964438a216d6b9b329bad8201175b83', placement='basiclite')
    resource(name='jdbc', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-jdbc-linux.x64-12.1.0.2.0.zip',
             md5='d3f4afd0dbf9b74c0b1e998dd69e6c9c', placement='jdbc')
    resource(name='odbc', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-odbc-linux.x64-12.1.0.2.0.zip',
             md5='30c72d4bca33084dcafe466ab1a7c399', placement='odbc')
    resource(name='sdk', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-sdk-linux.x64-12.1.0.2.0.zip',
             md5='d5eff6654c7901d2d5bccc87e386e192', placement='sdk')
    resource(name='sqlplus', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-sqlplus-linux.x64-12.1.0.2.0.zip',
             md5='f165280723ff1c96f825ba62c63b65cf', placement='sqlplus')
    resource(name='tools', url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/oracle/12.1.0.2.0/instantclient-tools-linux.x64-12.1.0.2.0.zip',
             md5='aff843e3748bf49cc063fa695cca9fd2', placement='tools')

    def install(self, spec, prefix):
        install_tree('sdk/sdk/include', prefix.include)
        mkdirp(self.prefix.lib)
        for f in glob.glob('*/lib*'):
            install(f, self.prefix.lib)
        mkdirp(self.prefix.bin)

        with working_dir(prefix.lib, create=False):
            for f in glob.glob('lib*.' + dso_suffix + '.[0-9]*'):
                dest = str(os.path.basename(f)).split(
                    '.')[0] + '.' + dso_suffix
                os.symlink(f, dest)

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

        fname = 'oracle.xml'
        template = Template("""<tool name="oracle" version="$VER">
  <lib name="clntsh"/>
  <client>
    <environment name="ORACLE_BASE" default="$PFX"/>
    <environment name="ORACLE_ADMINDIR" value="$PFX/etc"/>
    <environment name="LIBDIR" value="$$ORACLE_BASE/lib"/>
    <environment name="BINDIR" value="$$ORACLE_BASE/bin"/>
    <environment name="INCLUDE" value="$$ORACLE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
  <runtime name="TNS_ADMIN" default="$$ORACLE_ADMINDIR"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'oracleocci.xml'
        template = Template("""<tool name="oracleocci" version="$VER">
  <lib name="occi"/>
  <use name="oracle"/>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
