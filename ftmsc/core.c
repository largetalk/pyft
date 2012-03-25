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

static PyObject* pyQISRSessionBegin(PyObject *self, PyObject *args)
{
    const char *grammarList;
    const char *params;
    int err_code;

    const char* sessid;
    if (!PyArg_ParseTuple(args, "ss", &grammarList, &params))
        return NULL;

    sessid = QISRSessionBegin(grammarList, params, &err_code);
    return Py_BuildValue("si", sessid, err_code);
}


static PyMethodDef FtmscMethods[] = {  
    {"qisrInit", pyQISRInit, METH_VARARGS, "exec QISRInit"},  
    {"qisrSessionBegin", pyQISRSessionBegin, METH_VARARGS, "exec QISRSessionBegin"},
    {NULL, NULL, 0, NULL}  
};  

PyMODINIT_FUNC initcore(void)
{
    PyObject *m;
    m = Py_InitModule("ftmsc.core", FtmscMethods);
    if (m == NULL)
        return;
    FtmscError = PyErr_NewException("ftmsc.error", NULL, NULL);
    Py_INCREF(FtmscError);
    PyModule_AddObject(m, "error", FtmscError);
}

