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

#include <Core/Property.h>


namespace Core
{

class LX_CORE_EXPORT PropertyMD5 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const MD5& md5);

    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const MD5& getValue() const;

    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    MD5 _md5;
};


DECLARE_PROPERTY_FACTORY(PropertyMD5_Factory, Core::PropertyMD5);

}  // namespace Core
