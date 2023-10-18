#pragma once

#include <Base/Color.h>
#include <Base/GlobalId.h>
#include <Base/Type.h>
#include <Base/md5.h>
#include <Draw/Arrowheads.h>
#include <Draw/DrawStyle.h>
#include <Draw/OglMaterial.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>
#include <Draw/TextureCoordinateFunction.h>
#include <Draw/TextureCoordinateMapping.h>
#include <Geom/Ax2.h>
#include <Geom/Ax22d.h>
#include <Geom/Ax2d.h>
#include <Geom/BrepData.h>
#include <Geom/CompoundPlaneAngle.h>
#include <Geom/Dir.h>
#include <Geom/GTrsf.h>
#include <Geom/Pnt.h>
#include <Geom/Vec.h>

#include <any>
#include <unordered_set>



class QDateTime;
class QFont;

namespace Base
{
class AbstractWriter;
class AbstractXMLReader;
class PersistenceVersion;
}  // namespace Base

namespace LxIfcBase
{
class LxIfcEntity;
}

namespace Topo
{
class Shape;
}

namespace Geom
{
class Geometry;
}

namespace App
{
class Placement;
}

namespace Sketcher
{
class Constraint;
}

typedef std::shared_ptr<Topo::Shape> pShape;
typedef std::shared_ptr<Topo::Shape const> pConstShape;



namespace Core
{
class DocObject;
class CoreDocument;
struct ImportMessageDataType;
struct SearchValue;


class LX_CORE_EXPORT Variant
{
    explicit Variant(const char* s);  // private to forbid creating Variant(const char *), which creates Variant of Bool type without this constructor

public:
    friend class VariantHandler;
    friend class App::Placement;
    friend class Sketcher::Constraint;
    friend class Topo::Shape;

    enum Type
    {
        Undefined = 0,
        UInt8,
        UInt8List,
        UInt32,
        UInt64,
        Integer,
        IntegerList,
        Long,
        Double,
        StdString,
        String,
        Bool,
        StdStringList,
        StringList,
        MaterialList,
        Texture2List,
        Color,
        MColor,
        ColorList,
        MColorList,
        Texture2,
        Texture2Transform,
        TextureCoordinateMapping,
        TextureCoordinateFunction,
        DrawStyle,
        Arrowheads,
        Material,
        Object,
        ObjectSet,
        ObjectVector,
        Font,
        DateTime,
        DateTimeList,
        SearchSettings,
        SearchSettingsVector,
        Axis1,
        Axis2,
        Axis2d,
        Axis22d,
        Placement,
        Point,
        Point2d,
        Vector,
        Direction,
        Transform,
        GTransform,
        VectorList,
        PointList,
        Point2dList,
        Axis2List,
        Md5,
        BrepData,
        BrepDataSet,
        Shape,
        ConstShape,
        RealList,
        L2D_Placement,
        ListPointList,
        CompoundPlaneAngle,
        VariantList,
        GUID,
        ImportData,
        IfcEntity,
        LinkList,
        SketcherConstraintList,
        GeomGeometryList,
        CoreDocument,
        TypeMap,
        StringMap,
        String2DoubleMap,
        String2IntegerSetMap,
        ListVectorList,
        ListIntegerList,
        ListRealList,
        StringTable,
        User = 127
    };

    Variant();
    Variant(const Variant& in);
    explicit Variant(int i);
    explicit Variant(long i);
    explicit Variant(uint8_t i);
    explicit Variant(uint32_t i);
    explicit Variant(uint64_t i);
    explicit Variant(double d);
    // explicit Variant(const std::string &s);
    explicit Variant(const wchar_t* s);
    explicit Variant(const Base::String& s);
    // explicit Variant(const char *s);
    explicit Variant(bool b);
    explicit Variant(const Base::Color& c);
    explicit Variant(const Base::MColor& c);
    explicit Variant(const std::vector<Base::Color>& cl);
    explicit Variant(const std::vector<Base::MColor>& cl);
    explicit Variant(const Draw::OglMaterial& m);
    explicit Variant(const Draw::Texture2& t);
    explicit Variant(const Draw::Texture2Transform& ttf);
    explicit Variant(const Draw::TextureCoordinateMapping& tcm);
    explicit Variant(const Draw::TextureCoordinateFunction& tcf);
    explicit Variant(const Draw::DrawStyle& ds);
    explicit Variant(const Draw::Arrowheads& ah);
    explicit Variant(const std::list<std::string>& sl);
    explicit Variant(const std::list<Base::String>& sl);
    explicit Variant(const std::map<int, Draw::OglMaterial>& ml);
    explicit Variant(const std::map<int, Draw::Texture2>& tl);
    explicit Variant(const Geom::Ax1& ax1);
    explicit Variant(const Geom::Ax2& ax2);
    explicit Variant(const Geom::Ax2d& ax2d);
    explicit Variant(const Geom::Ax22d& ax22d);
    explicit Variant(Core::DocObject* o);
    explicit Variant(const std::unordered_set<Core::DocObject*>& oset);
    explicit Variant(const std::vector<Core::DocObject*>& objects);
    explicit Variant(const Geom::Pnt& p);
    explicit Variant(const Geom::Pnt2d& p);
    explicit Variant(const Geom::Vec& v);
    explicit Variant(const Geom::Dir& dir);
    explicit Variant(const Geom::Trsf& t);
    explicit Variant(const Geom::GTrsf& t);
    explicit Variant(const std::vector<int>& ilist);
    explicit Variant(const std::vector<uint8_t>& ilist);
    explicit Variant(const std::list<Geom::Vec>& vlist);
    explicit Variant(const std::vector<Geom::Pnt>& plist);
    explicit Variant(const std::vector<Geom::Pnt2d>& plist);
    explicit Variant(const std::list<Geom::Ax2>& vlist);
    explicit Variant(const MD5& v);
    explicit Variant(pBrepData data);
    explicit Variant(const std::vector<pBrepData>& dataSet);
    explicit Variant(pShape shape);
    explicit Variant(pConstShape shape);
    explicit Variant(const std::vector<double>& value);
    explicit Variant(const std::list<std::list<Geom::Pnt>>& the_list);
    explicit Variant(const std::list<std::list<Geom::Vec>>& the_list);
    explicit Variant(const std::list<std::list<int>>& the_list);
    explicit Variant(const std::list<std::list<double>>& the_list);
    explicit Variant(const Geom::CompoundPlaneAngle& compangle);
    explicit Variant(const std::vector<Core::Variant>& varList);
    explicit Variant(const Base::GlobalId& id);
    explicit Variant(const std::shared_ptr<ImportMessageDataType> aData);
    explicit Variant(const std::shared_ptr<LxIfcBase::LxIfcEntity> aEntity);
    explicit Variant(const std::list<Core::DocObject*>& list);
    explicit Variant(const std::vector<Geom::Geometry*>& aValue);
    explicit Variant(Core::CoreDocument* value);
    explicit Variant(const std::map<Base::Type, Core::DocObject*>& typeMap);
    explicit Variant(const std::map<Base::String, Base::String>& stringMap);
    explicit Variant(const std::map<Base::String, double>& string2doubleMap);
    explicit Variant(const std::map<Base::String, std::set<int>>& string2integerSetMap);
    explicit Variant(const std::vector<std::vector<Base::String>>& stringTable);

    ~Variant(void);

    bool operator==(const Variant& other) const;
    bool operator!=(const Variant& other) const;

    Variant::Type getType() const;
    /// Must be overwritten for custom types
    virtual int getUserType() const { return (int)getType(); }
    bool canConvert(Variant::Type t) const;
    uint64_t toUInt64(bool* ok = 0) const;
    uint32_t toUInt32(bool* ok = 0) const;
    uint8_t toUInt8(bool* ok = 0) const;
    int toInteger(bool* ok = 0) const;
    long toLong(bool* ok = 0) const;
    std::string toStdString(bool* ok = 0) const;
    Base::String toString(bool* ok = 0) const;
    double toDouble(bool* ok = 0) const;
    bool toBool(bool* ok = 0) const;
    Base::Color toColor(bool* ok = 0) const;
    std::vector<Base::Color> toColorList(bool* ok = 0) const;
    Draw::OglMaterial toMaterial(bool* ok = 0) const;
    Draw::Texture2 toTexture2(bool* ok = 0) const;
    Draw::Texture2Transform toTexture2Transform(bool* ok = 0) const;
    Draw::TextureCoordinateMapping toTextureCoordinateMapping(bool* ok = 0) const;
    Draw::TextureCoordinateFunction toTextureCoordinateFunction(bool* ok = 0) const;
    Draw::DrawStyle toDrawStyle(bool* ok = 0) const;
    Draw::Arrowheads toArrowheads(bool* ok = 0) const;
    std::list<std::string> toStdStringList(bool* ok = 0) const;
    std::list<Base::String> toStringList(bool* ok = 0) const;
    std::map<int, Draw::OglMaterial> toMaterialList(bool* ok = 0) const;
    std::map<int, Draw::Texture2> toTexture2List(bool* ok = 0) const;
    Geom::Ax1 toAxis1(bool* ok = 0) const;
    Geom::Ax2 toAxis2(bool* ok = 0) const;
    Geom::Ax2d toAxis2d(bool* ok = 0) const;
    Geom::Ax22d toAxis22d(bool* ok = 0) const;
    Core::DocObject* toObject(bool* ok = 0) const;
    Core::CoreDocument* toCoreDocument(bool* ok = 0) const;
    std::unordered_set<Core::DocObject*> toObjectSet(bool* ok = 0) const;
    std::vector<Core::DocObject*> toObjectVector(bool* ok = 0) const;
    Geom::Pnt toPoint(bool* ok = 0) const;
    Geom::Pnt2d toPoint2d(bool* ok = 0) const;
    Geom::Vec toVector(bool* ok = 0) const;
    Geom::Dir toDirection(bool* ok = 0) const;
    Geom::Trsf toTransform(bool* ok = 0) const;
    Geom::GTrsf toGTransform(bool* ok = 0) const;
    std::list<Geom::Vec> toVectorList(bool* ok = 0) const;
    std::vector<Geom::Pnt> toPointList(bool* ok = 0) const;
    std::vector<Geom::Pnt2d> toPoint2dList(bool* ok = 0) const;
    std::list<Geom::Ax2> toAxis2List(bool* ok = 0) const;
    MD5 toMD5(bool* ok = 0) const;
    pBrepData toBrepData(bool* ok = 0) const;
    std::vector<pBrepData> toBrepDataSet(bool* ok = 0) const;
    std::vector<int> toIntegerList(bool* ok = 0) const;
    std::vector<uint8_t> toUInt8List(bool* ok = 0) const;
    // pShape toShape(bool* ok = 0) const;
    std::vector<double> toRealList(bool* ok = 0) const;
    std::list<std::list<Geom::Pnt>> toListPointList(bool* ok = 0) const;
    std::list<std::list<Geom::Vec>> toListVectorList(bool* ok = 0) const;
    std::list<std::list<int>> toListIntegerList(bool* ok = 0) const;
    std::list<std::list<double>> toListRealList(bool* ok = 0) const;
    Geom::CompoundPlaneAngle toCompoundPlaneAngle(bool* ok = 0) const;
    std::vector<Core::Variant> toVariantList(bool* ok = 0) const;
    const std::shared_ptr<Core::ImportMessageDataType> toImportMessageDataType(bool* ok = 0) const;
    std::shared_ptr<LxIfcBase::LxIfcEntity> toIfcEntity(bool* ok = 0) const;
    std::list<Core::DocObject*> toLinkList(bool* ok = nullptr) const;
    std::vector<Geom::Geometry*> toGeomGeometryList(bool* ok = nullptr) const;
    std::map<Base::Type, Core::DocObject*> toTypeMap(bool* ok = nullptr) const;
    std::map<Base::String, Base::String> toStringMap(bool* ok = nullptr) const;
    std::map<Base::String, double> toString2DoubleMap(bool* ok = nullptr) const;
    std::map<Base::String, std::set<int>> toString2IntegerSetMap(bool* ok = nullptr) const;
    std::vector<std::vector<Base::String>> toStringTable(bool* ok = nullptr) const;

    /// Returns a string representation of the variant. If 'humanReadable=true' it returns a long version of the string, if 'false' it returns a short
    /// version for storing data. To get back the variants value from a string use the short version ('false')
    Base::String getAsString(bool humanReadable = true, int* version = 0) const;
    /// Returns variant type as string
    std::string getTypeAsString() const;

    bool hasValue() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) const;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version, const Base::String& variantType);

    /// The variant type
    int type;
    /// The data
    std::any data;

#ifndef SWIG

    explicit Variant(const QFont& font);
    explicit Variant(const QDateTime& dateTime);
    explicit Variant(const std::list<QDateTime>& dateTime);
    explicit Variant(const std::vector<std::vector<SearchValue>>& searchSettings);
    explicit Variant(const std::vector<std::vector<std::vector<SearchValue>>>& searchSettingsVector);

    QFont toFont(bool* ok = 0) const;
    QDateTime toDateTime(bool* ok = 0) const;
    std::list<QDateTime> toDateTimeList(bool* ok = 0) const;
    std::vector<std::vector<SearchValue>> toSearchSettings(bool* ok = 0) const;
    std::vector<std::vector<std::vector<SearchValue>>> toSearchSettingsVector(bool* ok = 0) const;

    Base::GlobalId toGUID(bool* ok = 0) const;

    template <typename T>
    T getValue(bool* ok) const
    {
        if (ok)
            *ok = true;
        return std::any_cast<T>(data);
    }
    template <>
    int getValue<int>(bool* ok) const
    {
        return toInteger(ok);
    }
    template <>
    uint32_t getValue<uint32_t>(bool* ok) const
    {
        return toUInt32(ok);
    }
    template <>
    long getValue<long>(bool* ok) const
    {
        return toLong(ok);
    }
    template <>
    std::string getValue<std::string>(bool* ok) const
    {
        return toStdString(ok);
    }
    template <>
    double getValue<double>(bool* ok) const
    {
        return toDouble(ok);
    }
    template <>
    bool getValue<bool>(bool* ok) const
    {
        return toBool(ok);
    }
    template <>
    Base::Color getValue<Base::Color>(bool* ok) const
    {
        return toColor(ok);
    }
    template <>
    Draw::OglMaterial getValue<Draw::OglMaterial>(bool* ok) const
    {
        return toMaterial(ok);
    }
    template <>
    Draw::Texture2 getValue<Draw::Texture2>(bool* ok) const
    {
        return toTexture2(ok);
    }
    template <>
    Draw::Texture2Transform getValue<Draw::Texture2Transform>(bool* ok) const
    {
        return toTexture2Transform(ok);
    }
    template <>
    Draw::TextureCoordinateMapping getValue<Draw::TextureCoordinateMapping>(bool* ok) const
    {
        return toTextureCoordinateMapping(ok);
    }
    template <>
    Draw::TextureCoordinateFunction getValue<Draw::TextureCoordinateFunction>(bool* ok) const
    {
        return toTextureCoordinateFunction(ok);
    }
    template <>
    Draw::DrawStyle getValue<Draw::DrawStyle>(bool* ok) const
    {
        return toDrawStyle(ok);
    }
    template <>
    Draw::Arrowheads getValue<Draw::Arrowheads>(bool* ok) const
    {
        return toArrowheads(ok);
    }
    template <>
    std::list<std::string> getValue<std::list<std::string>>(bool* ok) const
    {
        return toStdStringList(ok);
    }
    template <>
    std::list<Base::String> getValue<std::list<Base::String>>(bool* ok) const
    {
        return toStringList(ok);
    }
    template <>
    std::map<int, Draw::OglMaterial> getValue<std::map<int, Draw::OglMaterial>>(bool* ok) const
    {
        return toMaterialList(ok);
    }
    template <>
    std::map<int, Draw::Texture2> getValue<std::map<int, Draw::Texture2>>(bool* ok) const
    {
        return toTexture2List(ok);
    }
    template <>
    Geom::Ax1 getValue<Geom::Ax1>(bool* ok) const
    {
        return toAxis1(ok);
    }
    template <>
    Geom::Ax2 getValue<Geom::Ax2>(bool* ok) const
    {
        return toAxis2(ok);
    }
    template <>
    Geom::Ax2d getValue<Geom::Ax2d>(bool* ok) const
    {
        return toAxis2d(ok);
    }
    template <>
    Geom::Ax22d getValue<Geom::Ax22d>(bool* ok) const
    {
        return toAxis22d(ok);
    }
    /*template <>
    Core::Placement getValue<Core::Placement>(bool* ok) const { return toPlacement(ok); }	*/
    template <>
    Core::DocObject* getValue<Core::DocObject*>(bool* ok) const
    {
        return toObject(ok);
    }


    template <>
    std::unordered_set<Core::DocObject*> getValue<std::unordered_set<Core::DocObject*>>(bool* ok) const
    {
        return toObjectSet(ok);
    }
    template <>
    std::vector<Core::DocObject*> getValue<std::vector<Core::DocObject*>>(bool* ok) const
    {
        return toObjectVector(ok);
    }
    template <>
    std::map<Base::Type, DocObject*> getValue<std::map<Base::Type, DocObject*>>(bool* ok) const
    {
        return toTypeMap(ok);
    }
    template <>
    std::map<Base::String, Base::String> getValue<std::map<Base::String, Base::String>>(bool* ok) const
    {
        return toStringMap(ok);
    }
    template <>
    std::map<Base::String, double> getValue<std::map<Base::String, double>>(bool* ok) const
    {
        return toString2DoubleMap(ok);
    }
    template <>
    std::map<Base::String, std::set<int>> getValue<std::map<Base::String, std::set<int>>>(bool* ok) const
    {
        return toString2IntegerSetMap(ok);
    }
    template <>
    std::vector<std::vector<Base::String>> getValue<std::vector<std::vector<Base::String>>>(bool* ok) const
    {
        return toStringTable(ok);
    }

    // template <>
    // QFont getValue<QFont>(bool* ok) const { return toFont(ok); }
    // template <>
    // QDateTime getValue<QDateTime>(bool* ok) const { return toDateTime(ok); }
    template <>
    Geom::Pnt getValue<Geom::Pnt>(bool* ok) const
    {
        return toPoint(ok);
    }
    template <>
    Geom::Pnt2d getValue<Geom::Pnt2d>(bool* ok) const
    {
        return toPoint2d(ok);
    }
    template <>
    Geom::Vec getValue<Geom::Vec>(bool* ok) const
    {
        return toVector(ok);
    }
    template <>
    Geom::Dir getValue<Geom::Dir>(bool* ok) const
    {
        return toDirection(ok);
    }
    template <>
    Geom::Trsf getValue<Geom::Trsf>(bool* ok) const
    {
        return toTransform(ok);
    }
    template <>
    Geom::GTrsf getValue<Geom::GTrsf>(bool* ok) const
    {
        return toGTransform(ok);
    }
    template <>
    std::list<Geom::Vec> getValue<std::list<Geom::Vec>>(bool* ok) const
    {
        return toVectorList(ok);
    }
    template <>
    std::vector<Geom::Pnt> getValue<std::vector<Geom::Pnt>>(bool* ok) const
    {
        return toPointList(ok);
    }
    template <>
    std::vector<Geom::Pnt2d> getValue<std::vector<Geom::Pnt2d>>(bool* ok) const
    {
        return toPoint2dList(ok);
    }
    template <>
    std::list<Geom::Ax2> getValue<std::list<Geom::Ax2>>(bool* ok) const
    {
        return toAxis2List(ok);
    }
    template <>
    MD5 getValue<MD5>(bool* ok) const
    {
        return toMD5(ok);
    }
    template <>
    pBrepData getValue<pBrepData>(bool* ok) const
    {
        return toBrepData(ok);
    }
    template <>
    std::vector<pBrepData> getValue<std::vector<pBrepData>>(bool* ok) const
    {
        return toBrepDataSet(ok);
    }
    template <>
    std::vector<int> getValue<std::vector<int>>(bool* ok) const
    {
        return toIntegerList(ok);
    }
    /*template <>
    pShape getValue<pShape>(bool* ok) const { return toShape(ok); }*/
    // template <>
    // std::list<QDateTime> getValue< std::list<QDateTime> >(bool* ok) const { return toDateTimeList(ok); }
    template <>
    Base::GlobalId getValue<Base::GlobalId>(bool* ok) const
    {
        return toGUID(ok);
    }
    template <>
    std::shared_ptr<LxIfcBase::LxIfcEntity> getValue<std::shared_ptr<LxIfcBase::LxIfcEntity>>(bool* ok) const
    {
        return toIfcEntity(ok);
    }
    template <>
    std::list<Core::DocObject*> getValue<std::list<Core::DocObject*>>(bool* ok) const
    {
        return toLinkList(ok);
    }
    template <>
    std::vector<Geom::Geometry*> getValue<std::vector<Geom::Geometry*>>(bool* ok) const
    {
        return toGeomGeometryList(ok);
    }


#endif
};

LX_CORE_EXPORT std::ostream& operator<<(std::ostream& o, const Core::Variant& variant);

class LX_CORE_EXPORT VariantHandler
{
public:
    /// Creates a Variant
    virtual Core::Variant create() = 0;
    /// Compares, if two Variants, both of the same type, are equal.
    virtual bool isEqual(const Core::Variant& v1, const Core::Variant& v2, double tolerance = 1E-06) const = 0;
    /// Returns the Variant type
    virtual int getType() = 0;
    /// Returns a string representation of the value of the Variant
    virtual Base::String getAsString(const Core::Variant& v) const = 0;
    /// Returns the VariantHandler for this type
    static VariantHandler* getVariantHandler(int type);
    /// Registers a VariantHandler for a given type. returns true, if successful, false if a handler for this type exists already.
    static bool registerVariantHandler(int type, VariantHandler* vhnd);

private:
    static std::map<int, VariantHandler*> registry;
};

}  // Namespace Core
