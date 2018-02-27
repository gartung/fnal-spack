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
import glob

class Mcfm(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('6.3', git='https://github.com/cms-externals/MCFM', branch='cms/6.3')

    # FIXME: Add dependencies if required.
    depends_on('root')

    def install(self, spec, prefix):
        mkdirp('obj')
        filter_file(r'MCFMHOME.*=.*', 'MCFMHOME = %s' % self.stage.source_path, 'makefile')
        filter_file(r'HERE.*=.*','HERE = %s/QCDLoop' % self.stage.source_path, 'QCDLoop/makefile')
        filter_file(r'HERE.*= .*','HERE = %s/QCDLoop/ff' % self.stage.source_path, 'QCDLoop/ff/makefile')
        with working_dir(join_path(self.stage.source_path,'QCDLoop')):
            make('-j1')

        with working_dir(self.stage.source_path):
            make('-j1')
        os.remove('Bin/mcfm')
        mkdirp('lib')
        ar=which('ar')
        args=['cr','lib/libMCFM.a']
        for f in glob.glob('obj/*.o'):
            args.append(f)
        ar(*args)
        install_tree('lib',prefix.lib)
        install_tree('Bin',prefix.bin)
