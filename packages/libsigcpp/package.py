from spack import *


class Libsigcpp(Package):
    """Description"""

    homepage = "http://www.example.com"
    url = "http://ftp.acc.umu.se/pub/GNOME/sources/libsigc++/2.6/libsigc++-2.6.2.tar.xz"

    version('2.6.2', 'd2f33ca0b4b012ef60669e3b3cebe956')


    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
        cp = which('cp')
        cp(prefix + '/lib/sigc++-2.0/include/sigc++config.h',
           prefix + '/include/sigc++-2.0/')

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

        fname = 'sigcpp.xml'
        template = Template("""<tool name="sigcpp" version="$VER">
  <lib name="sigc-2.0"/>
  <client>
    <environment name="SIGCPP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$SIGCPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$SIGCPP_BASE/include/sigc++-2.0"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        contents = template.substitute(values)
        self.write_scram_toolfile(contents, fname)
