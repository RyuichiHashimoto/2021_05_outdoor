from distutils.core import setup, Extension

#setup(name = 'multiplyList', version = '1.0.0',  ext_modules = [Extension('multiplyList', ['py_list_list.cpp','find_closest.cpp'])])
setup(name = 'c_library', version = '1.0.0',  ext_modules = [Extension('c_library', ["python_library_setup.cpp",'external_lib.cpp','find_closest.cpp',"lib.cpp","merge_on_the_road.cpp"])])
