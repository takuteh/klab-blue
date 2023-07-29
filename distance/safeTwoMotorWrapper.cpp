#include <Python.h>

extern bool driveMotor(double, double, double);

PyObject* safeTwoMotor_driveMotor(PyObject* self, PyObject* args)
{
	double v1, v2, t;

	if (!PyArg_ParseTuple(args, "ddd", &v1, &v2, &t)) { return NULL; }
	bool result = driveMotor(v1, v2, t);
	return Py_BuildValue("O", result ? Py_True : Py_False);
}

static PyMethodDef safeTwoMotorMethods[] = {
	{"driveMotor", safeTwoMotor_driveMotor, METH_VARARGS},
	{NULL},
};

PyDoc_STRVAR(api_doc, "Drive motors with a distance sensor.\n");

static struct PyModuleDef cmodule = {
   PyModuleDef_HEAD_INIT,
   "safeTwoMotor",   /* name of module */
   api_doc, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   safeTwoMotorMethods
};

PyMODINIT_FUNC PyInit_safeTwoMotor(void)
{
    return PyModule_Create(&cmodule);
}