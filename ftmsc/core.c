#include <Python.h>
#include <stdio.h>
#include <string.h>
#include "qtts.h"
#include "qisr.h"

static PyObject *FtmscError;

static PyObject* pyQISRInit(PyObject *self, PyObject *args)
{
    const char *init_str;
    int ret;

    if (!PyArg_ParseTuple(args, "s", &init_str))
        return NULL;
	ret = QISRInit(init_str);
    return Py_BuildValue("i", ret);
}


static PyMethodDef FtmscMethods[] = {  
    {"qisr_init", pyQISRInit, METH_VARARGS, "exec QISRInit"},  
    {NULL, NULL, 0, NULL}  
};  

PyMODINIT_FUNC initftmsc(void)
{
    PyObject *m;
    m = Py_InitModule("ftmsc", FtmscMethods);
    if (m == NULL)
        return;
    FtmscError = PyErr_NewException("ftmsc.error", NULL, NULL);
    Py_INCREF(FtmscError);
    PyModule_AddObject(m, "error", FtmscError);
}

