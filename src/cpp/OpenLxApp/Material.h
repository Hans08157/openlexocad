#pragma once

#include <Core/PropertyAxis2.h>
#include <OpenLxApp/MaterialDefinition.h>
#include <OpenLxApp/MaterialSelect.h>


FORWARD_DECL(App, BimMaterial)

namespace OpenLxApp
{
/*!
 *
 * @brief Material is a homogeneous or inhomogeneous substance that can be used to form elements (physical products or their components).
 *
 * Material is the basic entity for material designation and definition; this includes identification by name and classification (via reference to an
 * external classification), as well as association of material properties (isotropic or anisotropic) defined by (subtypes of) IfcMaterialProperties.
 * An instance of IfcMaterial may be associated to an element or element type using the RelAssociatesMaterial relationship. The assignment might
 * either be direct as a single material information, or via
 *
 * - a material layer set
 * - a material profile set
 * - a material constituent set
 * A Material may also have presentation information associated. Such presentation information is provided by MaterialDefinitionRepresentation,
 * associating curve styles, hatching definitions or surface coloring/rendering information to a material. (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcmaterial.htm" target="_blank">Documentation from IFC4:
 * IfcMaterial</a>
 * @ingroup OPENLX_MATERIAL
 */

class LX_OPENLXAPP_EXPORT Material : public MaterialDefinition, public MaterialSelect
{
    PROXY_HEADER(Material, App::BimMaterial, IFCMATERIAL)

    DECL_PROPERTY(Material, Name, Base::String)
    DECL_PROPERTY(Material, Description, Base::String)
    DECL_PROPERTY(Material, Category, Base::String)


public:
    ~Material();

private:
    Material() {}
};

}  // namespace OpenLxApp
