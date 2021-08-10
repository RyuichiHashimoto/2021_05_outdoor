import ctypes as ct

libc = ct.cdll.LoadLibrary("./build/lib.linux-x86_64-3.7/module_name.cpython-37m-x86_64-linux-gnu.so")

libc.c_helloworld()

