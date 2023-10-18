#pragma once

#include <Core/DocObject.h>
namespace Core
{
class CoreDocument;
}

class QMutex;

namespace App
{
class ElementTool;
}


namespace Core
{

enum ExecuteStatus
{
    EXECUTE_OK = 0,
    EXECUTE_FAILED = 1
};

class LX_CORE_EXPORT ExecuteError
{
public:
    ExecuteError(Core::DocObject* obj, const std::string& m = "");
    Core::DocObject* obj;
    std::string msg;
};

class LX_CORE_EXPORT ExecuteContext
{
public:
    ExecuteContext(QMutex& aMutex) : mutex(aMutex) {}
    std::vector<Core::ExecuteError> objects_with_errors;
    // Holds an array of error message that are recorded when executing the object
    std::map<Core::DocObject*, std::vector<std::string> > errorMsgPerObject;

    bool throwException_On_Error = true;
    bool checkShape = true;
    bool checkFacetedBrep = false;
    bool checkSliverFaces = false;
    bool printErrorMessage = true;
    bool checkResultFromPolyToAcisConverter = false;  // PolyToAcisConverter has sometimes problems, removing loops etc
    int checkLevel = 20;
    double _tolerance = 10e-6;

#ifdef SWIG
	private:
#endif
    QMutex& mutex;
    void addErrorMsg(Core::DocObject* o, const std::string& msg);
};

class LX_CORE_EXPORT ExecObject : public Core::DocObject
{
    TYPESYSTEM_HEADER();
    LX_NODE_HEADER();
    // PROPERTYCONTAINER_HEADER( Core::ExecObject );

public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    friend class ::App::ElementTool;


    /// Is called when the document is recomputed
    virtual Core::ExecuteStatus execute(Core::ExecuteContext* context) = 0;
    /// Checks if the ExecObject is executable
    bool isExecutable() const override { return true; }
    /// Skips the execution of an ExecObject
    void skipExecution(bool yesno);
    /// Checks if the execution of the object is skipped
    bool skipExecution() const;

    /// Returns all ExecObjects that 'obj' directly or indirectly links to. Returns them ordered from bottom to top!
    static void getOrderedLinks(const Core::ExecObject* obj, std::vector<Core::ExecObject*>& ordered_links);
    /// Returns all ExecObjects that 'obj' directly links to.
    static void getLinks(const Core::ExecObject* obj, std::vector<Core::ExecObject*>& links);



protected:
    ExecObject();
    virtual ~ExecObject();

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API

private:
    bool _skipExecution;
    bool mOnlyVisibleHasChanged = false;


#endif
};


}  // namespace Core
