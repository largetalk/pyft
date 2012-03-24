from distutils.core import setup, Extension

base_module = Extension(name='ftmsc.core',
                    sources = ['ftmsc/core.c'],
                    include_dirs = ['.', './include'],
                    library_dirs = ['/usr/local/lib'],
                    libraries = ['speex','amr','amr_wb','dl', 'msc', 'pthread'])

setup (name = 'ftmsc',
       version = '0.1',
       description = 'this is a package for wrap flytek msc sdk',
       ext_modules = [base_module],
       author = 'Arthur',
       author_email = 'largetalk@gmail.com')
