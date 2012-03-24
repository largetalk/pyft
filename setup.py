import os
from os.path import join, isdir, abspath, basename, exists, dirname
from distutils.core import setup, Extension
from distutils.command import build_ext
import traceback

base_module = Extension(name='ftmsc.core',
                    sources = ['ftmsc/core.c'],
                    include_dirs = ['.', './include'],
                    library_dirs = ['/usr/local/lib'],
                    libraries = ['speex','amr','amr_wb','dl', 'msc', 'pthread'])

class my_build_ext(build_ext.build_ext):
    def initialize_options(self):
        build_ext.build_ext.initialize_options(self)
        
    def build_extension(self, ext):
        result = build_ext.build_ext.build_extension(self, ext)
        # hack: create a symlink from build/../core.so to gevent/core.so
        # to prevent "ImportError: cannot import name core" failures
        try:
            fullname = self.get_ext_fullname(ext.name)
            modpath = fullname.split('.')
            filename = self.get_ext_filename(ext.name)
            filename = os.path.split(filename)[-1]
            if not self.inplace:
                filename = os.path.join(*modpath[:-1] + [filename])
                path_to_build_core_so = abspath(os.path.join(self.build_lib, filename))
                path_to_core_so = abspath(join('ftmsc', basename(path_to_build_core_so)))
                if path_to_build_core_so != path_to_core_so:
                    try:
                        os.unlink(path_to_core_so)
                    except OSError:
                        pass
                    if hasattr(os, 'symlink'):
                        print 'Linking %s to %s' % (path_to_build_core_so, path_to_core_so)
                        os.symlink(path_to_build_core_so, path_to_core_so)
                    else:
                        print 'Copying %s to %s' % (path_to_build_core_so, path_to_core_so)
                        import shutil
                        shutil.copyfile(path_to_build_core_so, path_to_core_so)
        except Exception:
            traceback.print_exc()
            return result

setup (name = 'ftmsc',
       version = '0.1',
       description = 'this is a package for wrap flytek msc sdk',
       packages = ['ftmsc'],
       ext_modules = [base_module],
       cmdclass = {'build_ext': my_build_ext},
       author = 'Arthur',
       author_email = 'largetalk@gmail.com')
