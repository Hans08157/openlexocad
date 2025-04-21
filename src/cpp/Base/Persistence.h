#pragma once
#include <Base/Base.h>
#include <cassert>

namespace Base
{
class Reader;
class AbstractXMLReader;
class AbstractWriter;
class String;

class LX_BASE_EXPORT PersistenceVersion
{
public:
    int number = 0;
    int documentVersionMajor = 0;
    int documentVersionMinor = 0;
};

/// Persistence class and root of the type system
class LX_BASE_EXPORT Persistence : public Base::BaseClass
{
    TYPESYSTEM_HEADER();

public:
    /// This method is used to save properties or very small amounts of data to an XML document.
    virtual void save(Base::AbstractWriter& /*writer*/, Base::PersistenceVersion& /*save_version*/) = 0;

    /// This method is used to restore properties from an XML document.
    virtual void restore(Base::AbstractXMLReader& /*reader*/, Base::PersistenceVersion& /*version*/) = 0;

    /// This method is used to  save large amounts of data to a binary file.
    virtual void saveDocFile(Base::AbstractWriter& /*writer*/, const Base::String& /*filename*/, const Base::String& /*tmpdir*/) { assert(0); }
    /// This method is used to restore large amounts of data from a binary file.
    virtual void restoreDocFile(Base::Reader& /*reader*/, const Base::String& /*tmpdir*/) { assert(0); }
    /// Return 'true' if this object must always be saved in the file.
    virtual bool mustBeSaved() const { return false; }

    /// This method is used to save properties or very small amounts of data to an XML document.
    virtual bool createSQL(Base::AbstractWriter& /*writer*/, Base::PersistenceVersion& /*save_version*/, bool) { return false; }

    static std::string encodeAttribute(const std::string&);
};

}  // namespace Base
