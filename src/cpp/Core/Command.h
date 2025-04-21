///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once

#include <Base/Factory.h>
#include <Base/String.h>

#include <QObject>

namespace Core
{
class CommandP;
class Variant;

class LX_CORE_EXPORT Command

#ifndef SWIG
    : public QObject
#endif

{
public:

    

    Command();
    virtual ~Command();

    virtual bool redo() { return true; }
    virtual bool undo() { return true; }

    virtual void serialize(std::ostream& /*ar*/, unsigned int /*version*/);

    Base::String getDescription() const;
    void setDescription(const Base::String& s);

    void setParameter(const std::string& key, const Core::Variant& value);
    bool getParameter(const std::string& key, Core::Variant& value) const;

    void setSilentMode(bool on);
    bool isInSilentMode() const;

    void setDoRecomputeInRedo(bool on);
    void setDoRecomputeInUndo(bool on);
    bool getDoRecomputeInRedo() const;
    bool getDoRecomputeInUndo() const;

    void setDone(bool yes);
    bool isDone() const;

    long ____deadVal = 0xBADEAFFE;
private:
    std::unique_ptr<Core::CommandP> _pimpl;
    // DG, Debugging, after destructor, this value is 0xDEADBEEF
    
};




class LX_CORE_EXPORT CommandFactory : public Base::Factory<Core::Command, std::string>
{
    
public:
    Core::Command* CreatePublic(std::string id) { return Base::Factory<Core::Command, std::string>::Create(id); }

private:
    Core::Command* Create(std::string id) 
    { return Base::Factory<Core::Command, std::string>::Create(id); }

};

}  // namespace Core