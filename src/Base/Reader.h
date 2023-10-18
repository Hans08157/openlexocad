#pragma once
#include <Base/AbstractXMLReader.h>
#include <xercesc/sax2/DefaultHandler.hpp>
#include <xercesc/framework/XMLPScanToken.hpp>
#include <filesystem>
#include <map>

namespace XERCES_CPP_NAMESPACE
{
class SAX2XMLReader;
class Attributes;
class Locator;
class SAXParseException;
}

class QByteArray;

namespace Base
{


class LX_BASE_EXPORT XMLReader : public AbstractXMLReader, public XERCES_CPP_NAMESPACE::DefaultHandler
{
public:
    /// opens the file and read the first element
    XMLReader(const Base::String& FileName, std::istream&);
    ~XMLReader();

    inline bool isValid() const { return _valid; }

    /** @name Parser handling */
    //@{
    // read the next element
    inline void read(void);
    /// get the local name of the current Element
    inline const char* localName(void);
    /// reads until it findes a start element (<name>) or start-end element (<name/>) (with special name if given)
    inline void readElement(const char* ElementName = 0);
    /// reads until it findes a end element (with special name if given)
    inline void readEndElement(const char* ElementName = 0);
    /// reads until it findes characters
    inline void readCharacters(void);
    //@}

    /** @name Attribute handling */
    //@{
    /// get the numbers of attributes of the current Element
    inline unsigned int getAttributeCount(void) const;
    /// check if the read element has a special attribute
    inline bool hasAttribute(const char* AttrName) const;
    /// returns the named attribute as an interer (does type checking)
    inline long getAttributeAsInteger(const char* AttrName) const;
    /// returns the named attribute as an interer (does type checking)
    inline long getAttributeAsInteger(const wchar_t* AttrName) const;
    /// returns the named attribute as an double floating point (does type checking)
    inline double getAttributeAsDouble(const char* AttrName) const;
    /// returns the named attribute as an double floating point (does type checking)
    inline double getAttributeAsDouble(const wchar_t* AttrName) const;
    /// returns the named attribute as an double floating point (does type checking)
    inline Base::String getAttribute(const char* AttrName) const;
    /// returns the named attribute as an double floating point (does type checking)
    inline Base::String getAttribute(const wchar_t* AttrName) const;
    ///
    inline std::string getAttributeString(const char* AttrName) const;
    /// Returns the text of Characters
    inline Base::String getText();
    //@}

    virtual bool readInline() { return false; }

    


private:

    virtual void setDocumentLocator(const XERCES_CPP_NAMESPACE::Locator* const locator);

    // -----------------------------------------------------------------------
    //  Handlers for the SAX ContentHandler interface
    // -----------------------------------------------------------------------
    inline virtual void startElement(const XMLCh* const uri,
                                     const XMLCh* const localname,
                                     const XMLCh* const qname,
                                     const XERCES_CPP_NAMESPACE::Attributes& attrs);
    inline virtual void endElement(const XMLCh* const uri, const XMLCh* const localname, const XMLCh* const qname);
    inline virtual void characters(const XMLCh* const chars, const unsigned int length);
    inline virtual void ignorableWhitespace(const XMLCh* const chars, const unsigned int length);
    inline virtual void resetDocument();

    inline virtual void startCDATA();
    inline virtual void endCDATA();


    // -----------------------------------------------------------------------
    //  Handlers for the SAX ErrorHandler interface
    // -----------------------------------------------------------------------
    void warning(const XERCES_CPP_NAMESPACE::SAXParseException& exc);
    void error(const XERCES_CPP_NAMESPACE::SAXParseException& exc);
    void fatalError(const XERCES_CPP_NAMESPACE::SAXParseException& exc);
    void resetErrors();


    std::string LocalName;
    Base::String Characters;
    unsigned int CharacterCount;

    const XERCES_CPP_NAMESPACE::Attributes* m_attr;
    std::map<std::string, Base::String> AttrMap;
    typedef std::map<std::string, Base::String> AttrMapType;

    enum
    {
        None = 0,
        Chars,
        StartElement,
        StartEndElement,
        EndElement
    } ReadType;


    std::filesystem::path _File;
    XERCES_CPP_NAMESPACE::SAX2XMLReader* parser;
    XERCES_CPP_NAMESPACE::XMLPScanToken token;
    bool _valid;
    static bool isinit;
    Base::String _currentText;
    bool _CDATA_START;
    bool _CDATA_END;
    const XERCES_CPP_NAMESPACE::Locator* m_locator = 0;
};
}  // namespace Base

