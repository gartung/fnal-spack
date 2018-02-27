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
import os

class Blackhat(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://www.hepforge.org/archive/blackhat/blackhat-0.9.9.tar.gz"

    version('0.9.9', '64a4e64a95754bb701bf0c1f88c8ee53')

    patch('blackhat-gcc48.patch')
    patch('blackhat-0.9.9-armv7hl.patch')
    patch('blackhat-no_warnings.patch')
    patch('blackhat-0.9.9-default-arg-at-first-decl.patch')
    patch('blackhat-0.9.9-gcc600.patch')


    # FIXME: Add dependencies if required.
    depends_on('qd')
    depends_on('openssl')
    depends_on('python')

    def patch(self):
        if os.path.exists('./config/config.sub'):
            os.remove('./config/config.sub')
            install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
        if os.path.exists('./config/config.guess'):
            os.remove('./config/config.guess')
            install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')



    def install(self, spec, prefix):
        QD_ROOT=spec['qd'].prefix
        OPENSSL_ROOT=spec['openssl'].prefix
        configure('--prefix=%s' % prefix,
                '--with-QDpath=%s' % QD_ROOT,
                'CXXFLAGS=-Wno-deprecated -I%s/include' % OPENSSL_ROOT,
                'LDFLAGS=-L%s/lib' % OPENSSL_ROOT)
        make()
        make('install')

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

        fname = 'blackhat.xml'
        template = Template("""
<tool name="blackhat" version="${VER}">
<lib name="Ampl_eval"/>
<lib name="BG"/>
<lib name="BH"/>
<lib name="BHcore"/>
<lib name="CutPart"/>
<lib name="Cut_wCI"/>
<lib name="Cuteval"/>
<lib name="Integrals"/>
<lib name="Interface"/>
<lib name="OLA"/>
<lib name="RatPart"/>
<lib name="Rateval"/>
<lib name="Spinors"/>
<lib name="assembly"/>
<lib name="ratext"/>
<client>
<environment name="BLACKHAT_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$BLACKHAT_BASE/lib/blackhat"/>
<environment name="INCLUDE" default="$$BLACKHAT_BASE/include"/>
</client>
<use name="qd"/>
<runtime name="WORKER_DATA_PATH" value="$$BLACKHAT_BASE/share/blackhat/datafiles/" type="path"/>
</tool>
""")
        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)

