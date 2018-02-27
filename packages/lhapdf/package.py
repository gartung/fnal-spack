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
import tarfile
import os


class Lhapdf(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url = "http://www.hepforge.org/archive/lhapdf/LHAPDF-6.2.1.tar.gz"

    version('6.2.1', '9e05567d538fdb4862d4781cd076d7db')

    resource(name='cteq6l1', url='http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/cteq6l1.tar.gz',
             md5='5611f1e9235151d9f67254aeb13bb65f')
    resource(name='CT10', url='http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/CT10.tar.gz',
             md5='ec16da599329ad3525df040219c64538')
    resource(name='MSTW2008nlo68cl', url='http://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MSTW2008nlo68cl.tar.gz',
             md5='929cd57dbcd8bae900c2bf694c529d75')
    resource(name='MMHT2014lo68cl', url='https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014lo68cl.tar.gz',
             md5='25aae4cc0a0428de50fd6bdc5f7ff20b')
    resource(name='MMHT2014nlo68cl', url='https://www.hepforge.org/archive/lhapdf/pdfsets/6.1/MMHT2014nlo68cl.tar.gz',
             md5='71688543dd0a624944e023be0171c6e3')

    def patch(self):
        install(join_path(os.path.dirname(__file__), "lhapdf_makeLinks.file"),
                "lhapdf_makeLinks")
        install(join_path(os.path.dirname(__file__), "lhapdf_pdfsetsindex.file"),
                "lhapdf_pdfsetsindex")

    # FIXME: Add dependencies if required.
    depends_on('gmake', type='build')
    depends_on('boost@1.63.0')
    depends_on('cython', type='build')
    depends_on('python')
#    depends_on('yaml-cpp@0.5.1')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-boost=%s' % spec['boost'].prefix,
                  'PYTHON=%s/bin/python' % spec['python'].prefix,
                  'CYTHON=%s/bin/cython' % spec['cython'].prefix,
                  'PYTHONPATH=%s/lib/python2.7/site-packages' %
                  spec['cython'].prefix)
        make('all', 'PYTHONPATH=%s/lib/python2.7/site-packages' %
             spec['cython'].prefix)
        make('install', 'PYTHONPATH=%s/lib/python2.7/site-packages' %
                        spec['cython'].prefix)

        mkdirp(join_path(spec.prefix.share, 'LHAPDF'))
        for pdf in ['cteq6l1', 'CT10', 'MSTW2008nlo68cl', 'MMHT2014lo68cl', 'MMHT2014nlo68cl']:
            install_tree(pdf, join_path(spec.prefix.share, 'LHAPDF', pdf))

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

        fname = 'lhapdf.xml'
        template = Template("""
<tool name="lhapdf" version="${VER}">
  <lib name="LHAPDF"/>
  <client>
    <environment name="LHAPDF_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LHAPDF_BASE/lib"/>
    <environment name="INCLUDE" default="$$LHAPDF_BASE/include"/>
  </client>
  <runtime name="LHAPDF_DATA_PATH" value="$$LHAPDF_BASE/share/LHAPDF"/>
  <use name="yaml-cpp"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
