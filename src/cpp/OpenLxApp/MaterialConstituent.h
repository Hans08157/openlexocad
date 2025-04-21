#pragma once

#include <OpenLxApp/Material.h>
#include <OpenLxApp/MaterialDefinition.h>
#include <OpenLxApp/MaterialSelect.h>

FORWARD_DECL(App, MaterialConstituent)

namespace OpenLxApp
{
/*!
 *
 * @brief IfcMaterialConstituent is a single and identifiable part of an element which is constructed of a number of part (one or more) each having an
 * individual material. The association of the material constituent to the part is provided by a keyword as value of the Name attribute. In order to
 * identify and distinguish the part of the shape representation to which the material constituent applies the IfcProductDefinitionShape of the
 * element has to include instances of IfcShapeAspect, using the same keyword for their Name attribute.
 *
 * NOTE  See the "Material Use Definition" at the individual element to which an IfcMaterialConstituentSet may apply for a required or recommended
 * definition of such keywords as value for MaterialConstituent.Name. (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcmaterialconstituent.htm" target="_blank">Documentation from
 * IFC4: IfcMaterialConstituent</a>
 * @ingroup OPENLX_MATERIAL
 */

class LX_OPENLXAPP_EXPORT MaterialConstituent : public MaterialDefinition, public MaterialSelect
{
    PROXY_HEADER(MaterialConstituent, App::MaterialConstituent, IFCMATERIALCONSTITUENT)

    DECL_PROPERTY(MaterialConstituent, Name, Base::String)
    DECL_PROPERTY(MaterialConstituent, Description, Base::String)
    DECL_PROPERTY(MaterialConstituent, Fraction, double)
    DECL_PROPERTY(MaterialConstituent, Category, Base::String)

public:
    ~MaterialConstituent();

    void setMaterial(std::shared_ptr<Material> aMaterial);
    std::shared_ptr<Material> getMaterial() const;

private:
    MaterialConstituent() {}
};

}  // namespace OpenLxApp
