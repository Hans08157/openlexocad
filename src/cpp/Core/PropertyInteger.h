#pragma once 

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyInteger : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(int i);
    bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    int getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    int _nValue = 0;
};

class LX_CORE_EXPORT PropertyLong : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(long i);
    bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    long getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    long _nValue = 0L;
};

class LX_CORE_EXPORT PropertyUInt64 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(uint64_t i);
    bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    uint64_t getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    /// Returns the debug information for this property
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;

protected:
    uint64_t _nValue = 0;
};

class LX_CORE_EXPORT PropertyUInt32 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(uint32_t i);
    bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    uint32_t getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    /// Returns the debug information for this property
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;



protected:
    uint32_t _nValue = 0;
};

class LX_CORE_EXPORT PropertyUInt8 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(uint8_t i);
    bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    uint8_t getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    uint8_t _nValue = 0;
};



class LX_CORE_EXPORT PropertyNumberOfDecimals : public Core::PropertyInteger
{
    TYPESYSTEM_HEADER();
};


class LX_CORE_EXPORT PropertyIndex : public Core::PropertyInteger
{
    TYPESYSTEM_HEADER();
};

class LX_CORE_EXPORT PropertyCountMeasure : public Core::PropertyInteger
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyIndexList
//
//  A list of indexes
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyIndexList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<int>& list);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    bool hasIndex(int i) const;
    bool hasIndex(int i, int& order) const;
    void addIndex(int i);
    void removeIndex(int i);

    void setEmpty();
    bool isEmpty() const;
    size_t getSize() const;

    const std::vector<int>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(_indexList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<int> _indexList;
};

/////////////////////////////////////////////////
//
//  Core::PropertyListIndexList
//
//  A list of list of indexes
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyListIndexList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::list<std::list<int>>& list);

    void setValue(int num_i,
                  int num_j,
                  const std::vector<int>& vector);
    // This sets the _list given a vector and the number of lines/rows of the _list itself

    bool setValueFromVariant(const Core::Variant& value) override;

    void copyValue(Core::Property* p) override;

    void setEmpty();

    bool isEmpty() const;

    const std::list<std::list<int>>& getValue() const;

    const std::vector<int> getValue(int& num_i,
                                    int& num_j) const;
    // This returns a copy of the _list encoded in a vector and the number of lines/rows of the multidimensional array

    Core::Variant getVariant() const override;

    void save(Base::AbstractWriter& writer,
              Base::PersistenceVersion& save_version) override;

    virtual void save(std::ofstream& writer); // For test purposes

    void restore(Base::AbstractXMLReader& reader,
                 Base::PersistenceVersion& version) override;

    bool isEqual(const Property*) const override;

    Core::Property* copy() const override;

    void paste(const Core::Property& from) override;

protected:
    std::list<std::list<int>> _list;
};

class LX_CORE_EXPORT PropertyEnum : public Core::PropertyIndex
{
    TYPESYSTEM_HEADER();

public:
    /// Enumeration methods
    //@{
    /** setting the enumeration string list
     * The list is a NULL terminated array of pointers to a const char* string
     * \code
     * const char enums[] = {"Black","White","Other",NULL}
     * \endcode
     */
    void setEnums(const char** plEnums);
    /** set the enum by a string
     * is slower the setValue(long). Use long if possible
     */
    void setValue(const char* value);
    /** set directly the enum value
     * In DEBUG checks for boundaries.
     * Is faster then using setValue(const char*).
     */

    void setValue(int);
    /// get the value as string
    const char* getValueAsString(void) const;
    /// get all possible enum values as vector of strings
    std::vector<std::string> getEnumVector(void) const;
    /// get the pointer to the enum list
    const char** getEnums(void) const;
    void copyValue(Core::Property* p) override;
    bool isEqual(const Property*) const override;

    //@}
protected:
    const char** _enumArray = nullptr;
};


class LX_CORE_EXPORT PropertyUInt8List : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<uint8_t>& list);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void setEmpty();
    bool isEmpty() const;

    const std::vector<uint8_t>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(_indexList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<uint8_t> _indexList;
};

DECLARE_PROPERTY_FACTORY(PropertyInteger_Factory, Core::PropertyInteger);
DECLARE_PROPERTY_FACTORY(PropertyNumberOfDecimals_Factory, Core::PropertyNumberOfDecimals);
DECLARE_PROPERTY_FACTORY(PropertyIndex_Factory, Core::PropertyIndex);
DECLARE_PROPERTY_FACTORY(PropertyIndexList_Factory, Core::PropertyIndexList);
DECLARE_PROPERTY_FACTORY(PropertyListIndexList_Factory, Core::PropertyListIndexList);
DECLARE_PROPERTY_FACTORY(PropertyEnum_Factory, Core::PropertyEnum);
DECLARE_PROPERTY_FACTORY(PropertyCountMeasure_Factory, Core::PropertyCountMeasure);

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyIntegerOpt, Core::PropertyInteger);
DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyEnumOpt, Core::PropertyEnum);


}  // namespace Core
