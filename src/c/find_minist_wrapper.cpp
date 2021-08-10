#include<iostream>
#include "/usr/include/python3.6m/Python.h" 
using namespace std;




static PyObject* c_helloworld(PyObject* self, PyObject* args) 
{
    cout << "asdf"<<endl;
    return Py_None;
}

static PyMethodDef myMethods[] = {
    { "helloworld", c_helloworld, METH_NOARGS, "Prints Hello World" },
    { NULL }
};


// myModule definition struct
static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",
    "Python3 C API Module(Sample 1)",
    -1,
    myMethods
};

// Initializes myModule
PyMODINIT_FUNC PyInit_myModule(void)
{
    return PyModule_Create(&myModule);
}




int main(){
 
}
