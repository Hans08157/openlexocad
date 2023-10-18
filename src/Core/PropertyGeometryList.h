#pragma once 

#include <Core/Property.h>

namespace Core
{
class Geometry;

class LX_CORE_EXPORT PropertyGeometryList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    /**
     * A constructor.
     * A more elaborate description of the constructor.
     */
    PropertyGeometryList();

    /**
     * A destructor.
     * A more elaborate description of the destructor.
     */
    virtual ~PropertyGeometryList();

    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;
    Core::Variant getVariant(void) const override;
    virtual bool isEqual(const Property*) const override;
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

    bool setValue(const std::vector<Geom::Geometry*>&);

    /*!
     * Same as setValue().
     * Added for compability reason with Sketcher::SketchObject
     */
    bool setValues(const std::vector<Geom::Geometry*>&);
    const std::vector<Geom::Geometry*>& getValue() const;

    /*!
     * Same as getValue().
     * Added for compability reason with Sketcher::SketchObject
     */
    const std::vector<Geom::Geometry*>& getValues() const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);

    virtual void setSize(int newSize);
    virtual int getSize(void) const;

    /** Sets the property
     */
    void set1Value(int idx, std::unique_ptr<Geom::Geometry>&&);
    bool setSingleValue(const Geom::Geometry*);
    bool setValues(const std::vector<Geom::Geometry*>&&);

    /// index operator
    Geom::Geometry* operator[](const int idx) const { return mValueList[idx]; }

private:
    std::vector<Geom::Geometry*> mValueList;
};

}  // namespace Core
