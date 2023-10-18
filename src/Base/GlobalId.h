///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2017   Cadwork Informatik. All rights reserved.             //
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
#include <Base/GlobalId_Policy.h>

class QUuid;

namespace Base
{
class LX_BASE_EXPORT GlobalId
{
public:
    /// Creates an empty GlobalId.
    GlobalId();
    /// Creates a GlobalId from 22 char long base64 string. Expected format is '3x663a8XD65viEHNLVdTxd'. If 'aCheckBase64 == true' the string is
    /// checked if it was created from a valid GUID. If it wasn't created from a valid GUID, an exception is thrown.
    GlobalId(const Base::String& aBase64, bool aCheckBase64 = false);
    /// Creates a GlobalId from const char*. Expected format is '{F40650C2-4ACE-4606-89B1-DF4200C40E23}'.
    GlobalId(const char* aUniqueId);

    bool isNull() const;
    static GlobalId createGlobalId();
    static GlobalId fromQUuid(const QUuid& uuid);
    static void toQUuid(const GlobalId& in, QUuid& uuid);
    void toQUuid(QUuid& uuid) const;
    QUuid toQUuid() const;
    Base::String toBase64() const;
    Base::String toString() const;
    QString toQString() const;
    QString toQBase64() const;

    unsigned int data1;
    unsigned short data2;
    unsigned short data3;
    unsigned char data4[8];

    bool operator==(const GlobalId& rhs) const;
    bool operator!=(const GlobalId& rhs) const;
    bool operator<(const GlobalId& rhs) const;
    bool operator>(const GlobalId& rhs) const;

    friend std::size_t hash_value(GlobalId const& b) { return b.hash(); }

    size_t hash() const;
};
}  // namespace Base

namespace std
{
template <>
class hash<Base::GlobalId>
{
public:
    size_t operator()(const Base::GlobalId& id) const { return id.hash(); }
};
}  // namespace std
