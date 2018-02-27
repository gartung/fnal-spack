##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import shutil
import os


class Tkonlinesw(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://cms-trackerdaq-service.web.cern.ch/cms-trackerdaq-service/download/sources/trackerDAQ-4.1.0-1.tgz"

    version('4.1.0-1', 'aa8c780611f0292d5ff534d992617b46')

    depends_on('oracle')
    depends_on('xerces-c')
    depends_on('gmake')
    depends_on('root')

    def setup_environment(self, spack_env, run_env):
        projectname = 'trackerDAQ'
        releasename = str(self.stage.path) + '/' + \
            projectname + '-4.1-tkonline'
        spack_env.set('ENV_TRACKER_DAQ', releasename + '/opt/trackerDAQ')
        spack_env.set('XDAQ_ROOT', releasename + '/FecSoftwareV3_0/generic')
        spack_env.set('XDAQ_RPMBUILD', 'yes')
        spack_env.set('USBFEC', 'no')
        spack_env.set('PCIFEC', 'yes')
        spack_env.set('ENV_CMS_TK_BASE', releasename)
        spack_env.set('ENV_CMS_TK_DIAG_ROOT', releasename + '/DiagSystem')
        spack_env.set('ENV_CMS_TK_ONLINE_ROOT',
                      releasename + '/TrackerOnline/')
        spack_env.set('ENV_CMS_TK_COMMON', releasename +
                      '/TrackerOnline/2005/TrackerCommon/')
        spack_env.set('ENV_CMS_TK_XDAQ', releasename +
                      '/TrackerOnline/2005/TrackerXdaq/')
        spack_env.set('ENV_CMS_TK_APVE_ROOT',
                      releasename + '/TrackerOnline/APVe')
        spack_env.set('ENV_CMS_TK_FEC_ROOT', releasename + '/FecSoftwareV3_0')
        spack_env.set('ENV_CMS_TK_FED9U_ROOT', releasename +
                      '/TrackerOnline/Fed9U/Fed9USoftware')
        spack_env.set('ENV_CMS_TK_ICUTILS', releasename +
                      '/TrackerOnline/2005/TrackerCommon//ICUtils')
        spack_env.set('ENV_CMS_TK_LASTGBOARD', releasename + '/LAS')
        spack_env.set('ENV_CMS_TK_HAL_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('ENV_CMS_TK_CAEN_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('ENV_CMS_TK_SBS_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('ENV_CMS_TK_TTC_ROOT', '%s/dummy/Linux' %
                      self.spec.prefix)
        spack_env.set('XDAQ_OS', 'linux')
        spack_env.set('XDAQ_PLATFORM', 'x86_slc4')
        spack_env.set('CPPFLAGS', '-fPIC')
        spack_env.set('CFLAGS', '-O2 -fPIC')
        spack_env.set('CXXFLAGS', '-O2 -fPIC')

    def install(self, spec, prefix):
        filter_file('-Werror', '', 'FecSoftwareV3_0/generic/Makefile')
        mkdirp(join_path(prefix, 'dummy/Linux/lib'))
        configure('--with-xdaq-platform=x86_64',
                  '--with-oracle-path=%s' % spec['oracle'].prefix,
                  '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        with working_dir('FecSoftwareV3_0'):
            configure('--with-xdaq-platform=x86_64',
                      '--with-oracle-path=%s' % spec['oracle'].prefix,
                      '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        with working_dir('TrackerOnline/Fed9U/Fed9USoftware'):
            configure('--with-xdaq-platform=x86_64',
                      '--with-oracle-path=%s' % spec['oracle'].prefix,
                      '--with-xerces-path=%s' % spec['xerces-c'].prefix)
        make('cmssw')
        make('cmsswinstall')

        projectname = 'trackerDAQ'
        releasename = str(self.stage.path) + '/' + \
            projectname + '-4.1-tkonline'
        project_path = join_path(releasename, 'opt', projectname)
        install_tree(join_path(project_path, 'include'), prefix.include)
        install_tree(join_path(project_path, 'lib'), prefix.lib)

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

        fname = 'tkonlinesw.xml'
        template = Template("""
<tool name="TkOnlineSw" version="${VER}">
  <info url="http://www.cern.ch/"/>
  <lib name="ICUtils"/>
  <lib name="Fed9UUtils"/>
  <client>
    <environment name="TKONLINESW_BASE" default="${PFX}"/>
    <environment name="LIBDIR" value="$$TKONLINESW_BASE/lib"/>
    <environment name="INCLUDE" value="$$TKONLINESW_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-DCMS_TK_64BITS"/>
  <use name="root_cxxdefaults"/>
  <use name="xerces-c"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'tkonlineswdb.xml'
        template = Template("""
<tool name="TkOnlineSwDB" version="${VER}">
  <info url="http://www.cern.ch/"/>
  <lib name="DeviceDescriptions"/>
  <lib name="Fed9UDeviceFactory"/>
  <use name="tkonlinesw"/>
  <use name="oracle"/>
  <use name="oracleocci"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
