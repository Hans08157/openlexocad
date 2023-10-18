#pragma once 

#include <Core/PropertyString.h>


namespace Core
{
/* @brief An identifier is an alphanumeric string which allows an
 * individual thing to be identified. It may not provide natural-language meaning.
 *
 * Type: STRING of up to 255 characters
 */

class LX_CORE_EXPORT PropertyIdentifier : public Core::PropertyString
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyIdentifierOpt, Core::PropertyIdentifier);
DECLARE_PROPERTY_FACTORY(PropertyIdentifier_Factory, Core::PropertyIdentifier);

}  // namespace Core
