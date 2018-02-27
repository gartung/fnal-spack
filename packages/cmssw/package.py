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


def relrelink(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for x in files:
            p = os.path.join(root, x)
            f = os.path.abspath(p)
            if os.path.islink(f):
                linkto = os.path.realpath(f)
                if not os.path.commonprefix((f, linkto)) == '/':
                    rel = os.path.relpath(linkto, start=os.path.dirname(f))
                    os.remove(p)
                    os.symlink(rel, p)
        for y in dirs:
            p = os.path.join(root, y)
            f = os.path.abspath(p)
            if os.path.islink(f):
                linkto = os.path.realpath(f)
                if not os.path.commonprefix((f, linkto)) == '/':
                    rel = os.path.relpath(linkto, start=os.path.dirname(f))
                    os.remove(p)
                    os.symlink(rel, p)


class Cmssw(Package):
    """CMSSW built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc_amd64_gcc630/cms/cmssw/CMSSW_9_2_12/src.tar.gz"

    version('9.2.12', 'c66e3769785321309f70f85bc315e948')

    config_tag = 'V05-05-40'

    resource(name='config',
             url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/fwlite/CMSSW_9_2_13_FWLITE/%s.tar.gz' % config_tag,
             md5='87af022eba2084d0db2b4d92245c3629',
             placement='config'
             )

    depends_on('scram')
    depends_on('gmake')
    depends_on('root@6.08.07')
    depends_on('tbb')
    depends_on('tinyxml')
    depends_on('clhep@2.3.1.1~cxx11+cxx14')
    depends_on('md5')
    depends_on('python+shared')
    depends_on('vdt')
    depends_on('boost@1.63.0')
    depends_on('libsigcpp')
    depends_on('xrootd')
    depends_on('cppunit')
    depends_on('xerces-c')
    depends_on('expat')
    depends_on('sqlite')
    depends_on('bzip2')
    depends_on('gsl')
    depends_on('hepmc')
    depends_on('heppdt')
    depends_on('libpng')
    depends_on('giflib')
    depends_on('openssl')
    depends_on('pcre')
    depends_on('zlib')
    depends_on('xz')
    depends_on('libtiff')
    depends_on('libjpeg-turbo')
    depends_on('libxml2^python+shared')
    depends_on('bzip2')
    depends_on('fireworks-geometry')
    depends_on('llvm@4.0.1~gold~libcxx+python+shared_libs')
    depends_on('uuid-cms')
    depends_on('valgrind')
    depends_on('geant4~qt')
    depends_on('expat')
    depends_on('protobuf@3.2.0')
    depends_on('eigen')
    depends_on('curl')
    depends_on('classlib')
    depends_on('davix')
    depends_on('tcmalloc-fake')
    depends_on('meschach')
    depends_on('fastjet')
    depends_on('fastjet-contrib')
    depends_on('fftjet')
    depends_on('pythia6')
    depends_on('pythia8')
    depends_on('oracle')
    depends_on('sqlite@3.16.02')
    depends_on('coral')
    depends_on('hector')
    depends_on('geant4-g4emlow')
    depends_on('geant4-g4ndl')
    depends_on('geant4-g4photonevaporation')
    depends_on('geant4-g4saiddata')
    depends_on('geant4-g4abla')
    depends_on('geant4-g4ensdfstate')
    depends_on('geant4-g4neutronsxs')
    depends_on('geant4-g4radioactivedecay')
    depends_on('libhepml')
    depends_on('castor')
    depends_on('lhapdf')
    depends_on('utm')
    depends_on('tkonlinesw')
    depends_on('photospp')
    depends_on('rivet')
    depends_on('evtgen')
    depends_on('dcap')
    depends_on('tauolapp')
    depends_on('sherpa')
    depends_on('lwtnn')
    depends_on('yoda')
    depends_on('openloops')
    depends_on('qd')
    depends_on('blackhat')
    depends_on('yaml-cpp')
    depends_on('jemalloc')
    depends_on('ktjet')
    depends_on('herwig')
    depends_on('photos')
    depends_on('tauola')
    depends_on('jimmy')
    depends_on('cascade')
    depends_on('csctrackfinderemulation')
    depends_on('mcdb')
    depends_on('fftw') 
    depends_on('netlib-lapack')
 
    if sys.platform == 'darwin':
        patch('macos.patch')
    else:
        patch('linux.patch')

    scram_arch = 'linux_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'

    def install(self, spec, prefix):
        scram = which('scram')
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        scram_version = 'V' + str(spec['scram'].version)
        project_dir = join_path(prefix, cmssw_u_version)

        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['SELF_LIB'] = project_dir + '/lib/' + self.scram_arch
        values['SELF_INC'] = project_dir + '/src'
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()

        with working_dir(build_directory, create=True):
            install_tree(source_directory, 'src',
                         ignore=shutil.ignore_patterns('spack_build.*',
                                                       '.git', 'config'))
            install_tree(join_path(source_directory, 'config'), 'config',
                         ignore=shutil.ignore_patterns('.git'))
            with open('config/config_tag', 'w') as f:
                f.write(self.config_tag)
                f.close()
            mkdirp('tools/selected')
            mkdirp('tools/available')
            for dep in spec.dependencies():
                xmlfiles = glob(join_path(dep.prefix.etc, 'scram.d', '*.xml'))
                for xmlfile in xmlfiles:
                    install(xmlfile, 'tools/selected')
            perl = which('perl')
            perl('config/updateConfig.pl',
                 '-p', 'CMSSW',
                 '-v', cmssw_u_version,
                 '-s', scram_version,
                 '-t', build_directory,
                 '--keys', 'SCRAM_COMPILER=gcc',
                 '--keys', 'PROJECT_GIT_HASH=' + cmssw_u_version,
                 '--arch', self.scram_arch)
            scram('project', '-d', prefix, '-b', 'config/bootsrc.xml')

        with working_dir(project_dir, create=False):
            matches = []

            for f in glob('src/*/*/test/BuildFile*'):
                matches.append(f)
            for m in matches:
                if os.path.exists(m):
                    os.remove(m)

            scram.add_default_env('LOCALTOP', project_dir)
            scram.add_default_env('CMSSW_BASE', project_dir)
            scram.add_default_env(
                'LD_LIBRARY_PATH', project_dir + '/lib/' + self.scram_arch)
            scram.add_default_env(
                'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
            scram.add_default_env(
                'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)
            scram('build', '-v', '-k', '-j8')
            relrelink('external')
            shutil.rmtree('tmp')
#            install_tree(project_dir,prefix)


#        with working_dir(join_path(prefix,cmssw_u_version), create=False):
#            os.environ[ 'LOCALTOP' ] = os.getcwd()
#            os.environ[ 'RELEASETOP' ] = os.getcwd()
#            os.environ[ 'CMSSW_RELEASE_BASE' ] = os.getcwd()
#            os.environ[ 'CMSSW_BASE' ] = os.getcwd()
#            scram('build', 'ProjectRename')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        spack_env.set('LOCALTOP', self.prefix + '/' + cmssw_u_version)
        spack_env.set('RELEASETOP', self.prefix + '/' + cmssw_u_version)
        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix +
                              '/' + cmssw_u_version + '/lib/' + self.scram_arch)
        spack_env.append_path(
            'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

    def setup_environment(self, spack_env, run_env):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        spack_env.set('LOCALTOP', self.prefix + '/' + cmssw_u_version)
#        spack_env.set('RELEASETOP', self.prefix+'/'+cmssw_u_version)
#        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix +
                              '/' + cmssw_u_version + '/lib/' + self.scram_arch)
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
        spack_env.append_path(
            'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        version_underscore = str(self.version).replace('.', '_')
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/cms/cmssw/CMSSW_%s/src.tar.gz" % version_underscore
