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
import glob

class Openloops(SConsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/cms-externals/openloops/archive/v1.1.1.tar.gz"

    version('1.3.1', git='https://github.com/cms-externals/openloops', branch='cms/v1.3.1')
    version('1.2.3', git='https://github.com/cms-externals/openloops', branch='cms/v1.2.3')
    version('1.1.1', '1b87db455871014afed01d2193d8758c')
    version('1.0.1', '4b6381c8bc1b62855d604b1c37ed5189')

    depends_on('python', type='build')

    patch('openloops-1.2.3-cpp-use-undef.patch')

    def patch(self):
        contents="""
[OpenLoops]
import_env = @all
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0 -O0
loop_optimisation = -O0
generic_optimisation = -O0
born_optimisation = -O0
"""
        with open('openloops.cfg', 'w') as f:
            f.write(contents)
            f.close()

    def build(self, spec, prefix):
        builder = Executable('./openloops')
        builder('update', '--processes', 'generator=0')

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(join_path(prefix, 'proclib'))
        for f in glob.glob('lib/*.so'):
            install(f, join_path(prefix, f))
        for f in glob.glob('proclib/*.so'):
            install(f, join_path(prefix, f))
        for f in glob.glob('proclib/*.info'):
            install(f, join_path(prefix, f))


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

        fname = 'openloops.xml'
        template = Template("""
<tool name="openloops" version="${VER}">
<client>
<environment name="OPENLOOPS_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$OPENLOOPS_BASE/lib"/>
<runtime name="CMS_OPENLOOPS_PREFIX" value="$$OPENLOOPS_BASE" type="path"/>
</client>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
