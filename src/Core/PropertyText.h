#pragma once 

#include <Core/PropertyString.h>

namespace Core
{
class LX_CORE_EXPORT PropertyText : public Core::PropertyString
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyTextOpt, Core::PropertyText)

DECLARE_PROPERTY_FACTORY(PropertyText_Factory, Core::PropertyText);

}  // namespace Core
