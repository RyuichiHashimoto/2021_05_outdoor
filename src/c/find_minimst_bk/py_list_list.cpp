#include "/usr/include/python3.6m/Python.h" 
#include<vector>
#include<iostream>
#include"find_closest.hpp"
using namespace std;


Vec make_vector(PyObject *obj_list) {
    
    if(!PyList_Check(obj_list))
        return Vec(0);
    
    Vec v;
    const int   M = PyList_Size(obj_list);
    for(int j = 0; j < M; ++j) {
        // PyObject    *obj = PyList_GetItem(obj_list, (Py_ssize_t)j);
        PyObject    *obj = PyList_GetItem(obj_list, (Py_ssize_t)j);
        if(!PyFloat_Check(obj)) {
            printf("vector[%d] is not long.\n", j);
            return Vec(0);
        }        
        const double  d = PyFloat_AsDouble(obj);
        v.push_back(d);
    }
    return v;
}

Matrix make_matrix(PyObject *obj_table){
    
    if(!PyList_Check(obj_table)){
        return Matrix(0);
    }
    

    const int L = PyList_Size(obj_table);

    Matrix X(L);

    for (int i=0;i<L;i++){
        PyObject *obj = PyList_GetItem(obj_table, (Py_ssize_t)i);
        Vec v = make_vector(obj);
        if (v.empty()){
            printf("%d error has occured in make_matrix",i);
            return Matrix(0);
        }
        X[i] = v;
    }
    return X;
}


// C function "get list and return list"
static PyObject* find_closest(PyObject* self, PyObject* args)
{
    
    
    PyObject  *num,*grids;
    Matrix Mat_num,Mat_grids;
    
    if (!PyArg_ParseTuple(args, "OO", &num,&grids)){
        return NULL;
    }
        
    Mat_num = make_matrix(num);
    Mat_grids = make_matrix(grids);
    
    //  snap to grid
    vector<int> min_idx = find_closest_v2(Mat_num,Mat_grids);


    // ret value
    PyObject*  result_list,*item;
    result_list = PyList_New(min_idx.size());

    for(int i=0;i<(int)min_idx.size();i++){
        item = Py_BuildValue("l",min_idx[i]);
        PyList_SET_ITEM(result_list,i,item);        
    }

    return result_list;
}

// C function "get list and return list"
static PyObject* find_closest_using_v1(PyObject* self, PyObject* args)
{
    
    PyObject  *num,*grids;
    Matrix Mat_num,Mat_grids;
    
    if (!PyArg_ParseTuple(args, "OO", &num,&grids)){
        return NULL;
    }
        
    Mat_num = make_matrix(num);
    Mat_grids = make_matrix(grids);
    
    //  snap to grid
    vector<int> min_idx = find_closest_v1(Mat_num,Mat_grids);


    // ret value
    PyObject*  result_list,*item;
    result_list = PyList_New(min_idx.size());

    for(int i=0;i<(int)min_idx.size();i++){
        item = Py_BuildValue("l",min_idx[i]);
        PyList_SET_ITEM(result_list,i,item);        
    }

    return result_list;
}




// Function Definition struct
static PyMethodDef MultiplyList[] = {
    { "find_closest", find_closest, METH_VARARGS, "Multiply 2 and item of list "},
    { "find_closest_using_single_point", find_closest_using_v1, METH_VARARGS, "Multiply 2 and item of list "},        
    { NULL }
};

// Module Definition struct
static struct PyModuleDef multiplyList = {
    PyModuleDef_HEAD_INIT,
    "multiplyList",
    "Python3 C API Module(Sample 5)",
    -1,
    MultiplyList
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_multiplyList(void)
{
    return PyModule_Create(&multiplyList);
}