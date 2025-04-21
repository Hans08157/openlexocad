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

#include <Base/String.h>
#include <Core/StandardManipulatorPolicy.h>
#include <Geom/Pnt.h>

namespace Core
{
class DoubleResult
{
public:
    bool isNull() const { return _isNull; }
    double getValue() { return _value; }
    void setValue(double aValue)
    {
        _value = aValue;
        _isNull = false;
    }

private:
    bool _isNull = true;
    double _value;
};

class IntegerResult
{
public:
    bool isNull() const { return _isNull; }
    int getValue() { return _value; }
    void setValue(int aValue)
    {
        _value = aValue;
        _isNull = false;
    }

private:
    bool _isNull = true;
    int _value;
};

class StringResult
{
public:
    bool isNull() const { return _isNull; }
    Base::String getValue() { return _value; }
    void setValue(const Base::String& aValue)
    {
        _value = aValue;
        _isNull = false;
    }

private:
    bool _isNull = true;
    Base::String _value;
};

class PntResult
{
public:
    bool isNull() const { return _isNull; }
    Geom::Pnt getValue() { return _value; }
    void setValue(const Geom::Pnt& aValue)
    {
        _value = aValue;
        _isNull = false;
    }

private:
    bool _isNull = true;
    Geom::Pnt _value;
};

class StandardManipulatorPolicyResult
{
public:
    bool isNull() const { return _isNull; }
    Core::StandardManipulatorPolicy getValue() { return _value; }
    void setValue(const Core::StandardManipulatorPolicy& aValue)
    {
        _value = aValue;
        _isNull = false;
    }

private:
    bool _isNull = true;
    Core::StandardManipulatorPolicy _value;
};
}  // namespace Core
