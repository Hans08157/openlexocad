#pragma once

#include <Core/Variant.h>
#include <unordered_map>



namespace Core
{
class Property;

class LX_CORE_EXPORT PropertyValue  // Wraps property type and Core::Variant value
{
public:
    PropertyValue() : propertyName(""), propertyType(Base::Type::badType()), value(Core::Variant()) {}

    PropertyValue(const std::string& name, Base::Type t, const Core::Variant& v) : propertyName(name), propertyType(t), value(v) {}

    std::string propertyName;
    Base::Type propertyType;
    Core::Variant value;
};


typedef std::unordered_map<std::string, Core::Property*> PropertyMap;
typedef std::unordered_map<std::string, Core::PropertyValue> PropertyValueMap;

}  // namespace Core
