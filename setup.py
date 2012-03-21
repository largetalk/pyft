from distutils.core import setup, Extension

base_module = Extension('ftmsc',
                    sources = ['ftmscmodule.c'],
                    include_dirs = ['.', './include'],
                    library_dirs = ['./lib'],
                    libraries = ['amr', 'amr_wb', 'msc', 'speex'])

setup (name = 'ftmsc',
       version = '0.1',
       description = 'this is a package for wrap flytek msc sdk',
       ext_modules = [base_module],
       author = 'Arthur',
       author_email = 'largetalk@gmail.com')
