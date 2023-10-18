#pragma once

#include <Core/PropertyUser.h>

namespace Core
{
/*!
 * @brief Core::PropertyScriptParam is a class that can hold properties defined
 * by the user. Its value member is a Core::Variant and can hold
 * arbitrary information. It is used as parameters in Python Scripts
 */
class LX_CORE_EXPORT PropertyScriptParam : public Core::PropertyUser
{
    TYPESYSTEM_HEADER();

public:
    friend class PropertyScriptParam_Factory;

    bool setValueFromVariant(const Core::Variant& value) override;

    void onValueChanged();

private:
    int startScriptFunction(const std::string& aFunctionName, const Core::Variant& aValue);
    int callFunction(const char* aModuleName, const char* aFunctionName, const char* aCaller, const Core::Variant& aValue);
};

DECLARE_PROPERTY_FACTORY(PropertyScriptParam_Factory, Core::PropertyScriptParam);

}  // namespace Core
