#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
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

static PyObject* pyGrammarActivate(PyObject *self, PyObject *args)
{
    const char* sessid;
    const char* grammar;
    const char* type;
    int weight;
    int ret;

    if (!PyArg_ParseTuple(args, "sssi", &sessid, &grammar, &type, &weight))
        return NULL;

    ret = QISRGrammarActivate(sessid, grammar, type, weight);
    return Py_BuildValue("i", ret);
}

static PyObject* pyQISRAudioWrite(PyObject *self, PyObject *args)
{
    const char* sessid;
    const char* data;
    int dataLen;
    int audioStatus;
    int epStatus;
    int recogStatus;

    if (!PyArg_ParseTuple(args, "sz#i", &sessid, &data, &dataLen, &audioStatus))
        return NULL;

    int ret;
    ret = QISRAudioWrite(sessid, data, dataLen, audioStatus, &epStatus, &recogStatus);
    return Py_BuildValue("iii", ret, epStatus, recogStatus);
}

static PyObject* pyQISRGetResult(PyObject *self, PyObject *args)
{
    const char* sessid;
    int rsltStatus;
    int waitTime;
    int err;

    const char* strResult;

    if (!PyArg_ParseTuple(args, "si", &sessid, &waitTime))
        return NULL;

    strResult = QISRGetResult(sessid, &rsltStatus, waitTime, &err);
    return Py_BuildValue("iiz", err, rsltStatus, strResult);
}

static PyObject* pyQISRSessionEnd(PyObject *self, PyObject *args)
{
    const char* sessid;
    const char* hints;

    int ret;
    if (!PyArg_ParseTuple(args, "ss", &sessid, &hints))
        return NULL;

    ret = QISRSessionEnd(sessid, hints);
    return Py_BuildValue("i", ret);
}

static PyObject* pyQISRFini(PyObject *self, PyObject *args)
{
    int ret;
    ret = QISRFini();
    return Py_BuildValue("i", ret);
}

static PyMethodDef FtmscMethods[] = {  
    {"qisrInit", pyQISRInit, METH_VARARGS, "exec QISRInit"},  
    {"qisrSessionBegin", pyQISRSessionBegin, METH_VARARGS, "exec QISRSessionBegin"},
    {"qisrGrammarActive", pyGrammarActivate, METH_VARARGS, "exec GrammarActive"},
    {"qisrAudioWrite", pyQISRAudioWrite, METH_VARARGS, "exec AudioWrite"},
    {"qisrGetResult", pyQISRGetResult, METH_VARARGS, "exec GetResult"},
    {"qisrSessionEnd", pyQISRSessionEnd, METH_VARARGS, "exec SessionEnd"},
    {"qisrFini", pyQISRFini, METH_VARARGS, "exec QISRFini"},
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

