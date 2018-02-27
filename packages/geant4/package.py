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
import platform
import glob
import os


class Geant4(CMakePackage):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url = "http://geant4.cern.ch/support/source/geant4.10.01.p03.tar.gz"

    version('10.02.p02', git='https://github.com/cms-externals/geant4', branch='cms/v10.02.p02')

    variant('qt', default=False, description='Enable Qt support')
    variant('vecgeom', default=False, description='Enable Vecgeom support')

    depends_on('cmake@3.5:', type='build')

    depends_on("clhep@2.3.1.1~cxx11+cxx14")
    depends_on("expat")
    depends_on("zlib")
    depends_on("xerces-c")
    depends_on("qt@4.8:", when="+qt")
    depends_on("vecgeom", when="+vecgeom")
    # G4 data
    depends_on("geant4-g4emlow")
    depends_on("geant4-g4ndl")
    depends_on("geant4-g4photonevaporation")
    depends_on("geant4-g4saiddata")
    depends_on("geant4-g4abla")
    depends_on("geant4-g4ensdfstate")
    depends_on("geant4-g4neutronsxs")
    depends_on("geant4-g4radioactivedecay")

    def cmake_args(self):
        spec = self.spec

        options = [ '-DCMAKE_CXX_COMPILER=g++'
                   ,'-DCMAKE_CXX_FLAGS=-fPIC'
                   ,'-DCMAKE_INSTALL_LIBDIR=lib'
                   ,'-DCMAKE_BUILD_TYPE=Release'
                   ,'-DGEANT4_USE_GDML=ON'
                   ,'-DGEANT4_BUILD_CXXSTD:STRING=c++14'
                   ,'-DGEANT4_BUILD_TLS_MODEL:STRING=global-dynamic'
                   ,'-DGEANT4_ENABLE_TESTING=OFF'
                   ,'-DGEANT4_BUILD_VERBOSE_CODE=OFF'
                   ,'-DBUILD_SHARED_LIBS=ON'
                   ,'-DXERCESC_ROOT_DIR:PATH=%s' %
                     spec['xerces-c'].prefix
                   ,'-DCLHEP_ROOT_DIR:PATH=%s' %
                     spec['clhep'].prefix
                   ,'-DEXPAT_INCLUDE_DIR:PATH=%s' %
                     spec['expat'].prefix.include
                   ,'-DEXPAT_LIBRARY:FILEPATH=%s/libexpat.%s' % 
                     (spec['expat'].prefix.lib, dso_suffix)
                   ,'-DBUILD_STATIC_LIBS=ON'
                   ,'-DGEANT4_INSTALL_EXAMPLES=OFF'
                   ,'-DGEANT4_USE_SYSTEM_CLHEP=ON'
                   ,'-DGEANT4_BUILD_MULTITHREADED=ON'
                   ,'-DCMAKE_STATIC_LIBRARY_CXX_FLAGS=-fPIC'
                   ,'-DCMAKE_STATIC_LIBRARY_C_FLAGS=-fPIC' ]

        if '+vecgeom' in spec:
            options.append('-DGEANT4_USE_USOLIDS=ON')
            options.append('-DUSolids_DIR=%s' %
                           join_path(spec['vecgeom'].prefix, 'lib/CMake/USolids'))

        arch = platform.system().lower()
        if arch is not 'darwin':
            options.append('-DGEANT4_USE_OPENGL_X11=ON')
            options.append('-DGEANT4_USE_XM=ON')
            options.append('-DGEANT4_USE_RAYTRACER_X11=ON')

        if '+qt' in spec:
            options.append('-DGEANT4_USE_QT=ON')
            options.append(
                '-DQT_QMAKE_EXECUTABLE=%s' %
                spec['qt'].prefix + '/bin/qmake'
            )

        return options


    def url_for_version(self, version):
        """Handle Geant4's unusual version string."""
        return ("http://geant4.cern.ch/support/source/geant4.%s.tar.gz" % version)


    def write_scram_toolfile(self, contents, filename):
        """Write scram tool config file"""
        with open(self.spec.prefix.etc + '/scram.d/' + filename, 'w') as f:
            f.write(contents)
            f.close()

    @run_after('install')
    def make_archive_dir(self):
        mkdirp(self.prefix.lib+'/archive')
        with working_dir(self.prefix.lib+'/archive'):
            ar=which('ar')
            for f in glob.glob(self.prefix.lib+'/*.a'):
                ar('x', f)
            args = ['rcs', 'libgeant4-static.a']
            for f in glob.glob('*.o'):
                args.append(f)
            ar(*args)
            for f in glob.glob('*.o'):
                os.remove(f)

    @run_after('install')
    def write_scram_toolfiles(self):
        """Create contents of scram tool config files for this package."""
        from string import Template

        mkdirp(join_path(self.spec.prefix.etc, 'scram.d'))

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'geant4.xml'
        template = Template("""
<tool name="geant4" version="${VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <use name="geant4core"/>
  <use name="geant4vis"/>
  <use name="xerces-c"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'geant4core.xml'
        template = Template("""
<tool name="geant4core" version="${VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4digits_hits"/>
  <lib name="G4error_propagation"/>
  <lib name="G4event"/>
  <lib name="G4geometry"/>
  <lib name="G4global"/>
  <lib name="G4graphics_reps"/>
  <lib name="G4intercoms"/>
  <lib name="G4interfaces"/>
  <lib name="G4materials"/>
  <lib name="G4parmodels"/>
  <lib name="G4particles"/>
  <lib name="G4persistency"/>
  <lib name="G4physicslists"/>
  <lib name="G4processes"/>
  <lib name="G4readout"/>
  <lib name="G4run"/>
  <lib name="G4tracking"/>
  <lib name="G4track"/>
  <lib name="G4analysis"/>
  <flags CXXFLAGS="-DG4MULTITHREADED -DG4USE_STD11 -ftls-model=global-dynamic -pthread"/>
  <client>
    <environment name="GEANT4_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$GEANT4_BASE/lib"/>
    <environment name="G4LIB" value="$$LIBDIR"/>
    <environment name="INCLUDE" default="$$GEANT4_BASE/include/Geant4"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <flags cppdefines="GNU_GCC G4V9"/>
  <use name="clhep"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'geant4data.xml'
        template = Template("""
<tool name="geant4data" version="${VER}">
  <use name="geant4data_g4abla"/>
  <use name="geant4data_g4emlow"/>
  <use name="geant4data_g4ensdfstate"/>
  <use name="geant4data_g4ndl"/>
  <use name="geant4data_g4neutronsxs"/>
  <use name="geant4data_g4photonevaporation"/>
  <use name="geant4data_g4radioactivedecay"/>
  <use name="geant4data_g4saiddata"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'geant4vis.xml'
        template = Template("""
<tool name="geant4vis" version="${VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4FR"/>
  <lib name="G4modeling"/>
  <lib name="G4RayTracer"/>
  <lib name="G4Tree"/>
  <lib name="G4visHepRep"/>
  <lib name="G4vis_management"/>
  <lib name="G4visXXX"/>
  <lib name="G4VRML"/>
  <lib name="G4GMocren"/>
  <lib name="G4zlib"/>
  <use name="geant4core"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

        fname = 'geant4static.xml'
        template = Template("""
<tool name="geant4static" version="${VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="geant4-static"/>
  <flags CXXFLAGS="-DG4MULTITHREADED -DG4USE_STD11  -ftls-model=global-dynamic -pthread"/>
  <client>
    <environment name="GEANT4STATIC_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$GEANT4STATIC_BASE/lib/archive"/>
  </client>
  <use name="clhep"/>
  <use name="xerces-c"/>
</tool>
""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
