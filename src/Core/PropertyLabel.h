#pragma once 

#include <Core/PropertyString.h>


namespace Core
{
/* @brief A label is the term by which something may be referred to.
 * It is a string which represents the human-interpretable name of something
 * and shall have a natural-language meaning.
 *
 * Type: STRING of up to 255 characters
 */

class LX_CORE_EXPORT PropertyLabel : public Core::PropertyString
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyLabelOpt, Core::PropertyLabel);
DECLARE_PROPERTY_FACTORY(PropertyLabel_Factory, Core::PropertyLabel);

}  // namespace Core
