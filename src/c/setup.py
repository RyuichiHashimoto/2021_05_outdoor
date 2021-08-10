from distutils.core import setup, Extension
 
setup(name = 'c_helloworld', version = '1.0.0',  ext_modules = [Extension('other', ['other.c'])])