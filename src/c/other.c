

//Cの方で作成してPythonで利用する関数はPyObjectを使う

static PyObject* 
hello_world (PyObject *self, PyObject *args) {
  printf("Hello_world\n");
  // C側で作成する関数のreturnはPy~~...となる
  Py_RETURN_NONE;
}

static PyObject*
push(PyObject *self, PyObject *args){
  PyObject *p_list, *inthert_val, *receive_list;
  // 送られてきた値をパース
  if(!PyArg_ParseTuple(args, "O!i", &PyList_Type, &p_list, &inthert_val))
    return NULL;
  // 配列を抽出
  receive_list = PySequence_List(p_list);
  // 配列に値を追加
  printf("%dをpushします\n", inthert_val);
  PyList_Append(receive_list, Py_BuildValue("i", inthert_val));

  // 配列を返却
  return receive_list;
}

static PyObject*
pop (PyObject *self, PyObject *args){
  PyObject *p_list, *p_value;
  int size;
  long val;
  // 送られてきた値をパース
  if(!PyArg_ParseTuple(args, "O!", &PyList_Type, &p_list))
    return NULL;
  // リストのサイズ取得
  size = PyList_Size(p_list);
  //値を抽出 
  p_value = PyList_GetItem(p_list, size - 1);
  val = PyLong_AsLong(p_value);
  printf("%dをpopします\n", val);

  // 値を返却
  return p_value;
}

// メソッドの定義
static PyMethodDef PracticeMethods[] = {
  {"hello_world", (PyCFunction)hello_world, METH_NOARGS, "practice1: hello_world"},
  {"push", (PyCFunction)push, METH_VARARGS, "practice2: push"},
  {"pop", (PyCFunction)pop, METH_VARARGS, "practice3: pop"},
  // 終了を示す
  {NULL, NULL, 0, NULL}
};

//モジュールの定義
static struct PyModuleDef practicetmodule = {
  PyModuleDef_HEAD_INIT,
  "practice",
  NULL,
  -1,
  PracticeMethods
};

// メソッドの初期化
PyMODINIT_FUNC PyInit_practice (void) {
  return PyModule_Create(&practicetmodule);
}
