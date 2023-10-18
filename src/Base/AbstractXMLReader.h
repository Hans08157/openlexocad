#pragma once
#include <Base/String.h>

namespace Base
{
class LX_BASE_EXPORT AbstractXMLReader
{
public:
    virtual ~AbstractXMLReader() = default;
    virtual bool isValid() const = 0;
    virtual void read(void) = 0;
    virtual const char* localName(void) = 0;
    virtual void readElement(const char* ElementName = 0) = 0;
    virtual void readEndElement(const char* ElementName = 0) = 0;
    virtual void readCharacters(void) = 0;
    virtual unsigned int getAttributeCount(void) const = 0;
    virtual bool hasAttribute(const char* AttrName) const = 0;
    virtual long getAttributeAsInteger(const char* AttrName) const = 0;
    virtual long getAttributeAsInteger(const wchar_t* AttrName) const = 0;
    virtual double getAttributeAsDouble(const char* AttrName) const = 0;
    virtual double getAttributeAsDouble(const wchar_t* AttrName) const = 0;
    virtual Base::String getAttribute(const char* AttrName) const = 0;
    virtual Base::String getAttribute(const wchar_t* AttrName) const = 0;
    virtual std::string getAttributeString(const char* AttrName) const = 0;
    virtual Base::String getText() = 0;
    virtual bool readInline() = 0;
};
}  // namespace Base
