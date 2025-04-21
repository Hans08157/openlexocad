/*
copyright 2003 Jim Bublitz <jbublitz@nwinternet.com>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public License
along with this library; see the file COPYING.LIB.  If not, write to
the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
*/

#pragma once 

#include <string>
// Pythonize is a general purpose library that wraps the Python
// interpreter with an interface to a set of common operations
// used when embedding the interpreter.

namespace Base
{
class String;
}

typedef struct _ts PyThreadState;
typedef struct _object PyObject;


namespace Core
{
struct ObjectRef
{
    ObjectRef(ObjectRef* oi, PyObject* o);
    ~ObjectRef();

    PyObject* object = nullptr;       // pointer to an object we created
    ObjectRef* prevObject = nullptr;  // pointer to next object on the stack
};

class LX_CORE_EXPORT Pythonize
{
public:
    explicit Pythonize(const Base::String& pythonHome);
    ~Pythonize();

    // adds a path to sys.path
    bool appendToSysPath(const Base::String& newPath) const;

    // insert a path to sys.path
    bool insertToSysPath(int pos, const Base::String& newPath) const;

    // imports a module into the interpreter
    // or gets a PyObject for an already loaded module
    PyObject* importModule(char* moduleName);

    // returns an object from a loaded module
    // you must decref the object returned when done with it (new reference returned)
    PyObject* getNewObjectRef(PyObject* module, char* object) const;
    PyObject* getSysModule() const;
    PyObject* getMainModule() const;

    void setMainModule();
    bool getPythonInit() const;

    // runs a script on the current sys.path
    bool runScript(const Base::String& scr) const;
    bool runScript2(const Base::String& scr, Base::String& error) const;

    // executes a string of Python in the interpreter
    bool runString(const Base::String& str) const;
    bool runString2(const Base::String& str, Base::String& err) const;
    bool runString3(std::string input, std::string resultname, bool& result) const;
    bool runStringWithNameSpace(char* str, char* ns) const;

    std::string getPythonErrorString() const;

    // runs a callable Python object
    PyObject* runFunction(PyObject* object, PyObject* args) const;

    // handle the thread state and global interpreter lock
    void releaseLock() const;
    void acquireLock() const;
    PyThreadState* getThreadState() const;
    PyThreadState* setThreadState(PyThreadState* tstate) const;

    int runExpression(const Base::String& command, double& val) const;

private:
    bool _pythonInit = false;         // status of Py_Initialize
    PyObject* _sysModule = nullptr;   // a pointer to the sys module which is always loaded first
    PyObject* _mainModule = nullptr;  // a pointer to __main__
    ObjectRef* _objects = nullptr;    // a stack of PyObjects (used in destructor)
};
}  // namespace Core
