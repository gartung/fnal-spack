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


class Rivet(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/MCGeneratorsTarFiles/Rivet-2.5.4.tar.bz2"

    version('3.0.0alpha1', '7fb24d0e6ac8e9fe549d61194cb863d0')
    version('2.5.4',       '709a5c744135639f8f8195a1241ae81d', preferred=True)

    depends_on('hepmc')
    depends_on('fastjet')
    depends_on('gsl')
    depends_on('yoda')
    depends_on('boost')
    depends_on('py-cython')

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = ['--disable-silent-rules',
                '--with-hepmc=%s' % self.spec['hepmc'].prefix,
                '--with-fastjet=%s' % self.spec['fastjet'].prefix,
                '--with-gsl=%s' % self.spec['gsl'].prefix,
                '--with-yoda=%s' % self.spec['yoda'].prefix,
                '--disable-doxygen',
                '--disable-pdfmanual',
                '--with-pic',
                'PYTHONPATH=%s/lib/python2.7/site-packages' % self.spec['py-cython'],
                'CPPFLAGS=-I%s' % self.spec['boost'].prefix.include
                ]
        return args


    def write_scram_toolfile(self, contents,filename):
        """Write scram tool config file"""
        mkdirp(self.spec.prefix.etc+'/scram.d')
        with open(self.spec.prefix.etc+'/scram.d/'+filename,'w') as f:
            f.write(contents)
            f.close()


    @run_after('install')
    def write_scram_toolfiles(self):
        from string import Template
        pyvers=str(self.spec['python'].version).split('.')
        pyver=pyvers[0]+'.'+pyvers[1]
        values={}
        values['VER']=self.spec.version
        values['PFX']=self.spec.prefix
        values['PYVER']=pyver
        fname='rivet.xml'
        template=Template("""
<tool name="rivet" version="${VER}">
<lib name="Rivet"/>
<client>
<environment name="RIVET_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$RIVET_BASE/lib"/>
<environment name="INCLUDE" default="$$RIVET_BASE/include"/>
</client>
<runtime name="PATH" value="$$RIVET_BASE/bin" type="path"/>
<runtime name="PYTHONPATH" value="$$RIVET_BASE/lib/python${PYVER}/site-packages" type="path"/>
<runtime name="RIVET_ANALYSIS_PATH" value="$$RIVET_BASE/lib" type="path"/>
<runtime name="PDFPATH" default="$$RIVET_BASE/share" type="path"/>
<runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
<runtime name="TEXMFHOME" value="$$RIVET_BASE/share/Rivet/texmf" type="path"/>
<use name="hepmc"/>
<use name="fastjet"/>
<use name="gsl"/>
<use name="yoda"/>
</tool>
""")
        contents=template.substitute(values)
        self.write_scram_toolfile(contents,fname)
