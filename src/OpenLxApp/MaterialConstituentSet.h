#pragma once

#include <OpenLxApp/MaterialConstituent.h>
#include <OpenLxApp/MaterialDefinition.h>
#include <OpenLxApp/MaterialSelect.h>

FORWARD_DECL(App, MaterialConstituentSet)

namespace OpenLxApp
{
/*!
 *
 * @brief MaterialConstituentSet is a collection of individual material constituents, each assigning a material to a part of an element.
 * The parts are only identified by a keyword (as opposed to an MaterialLayerSet or MaterialProfileSet where each part has an individual
 * shape parameter (layer thickness or layer profile).
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcmaterialconstituentset.htm" target="_blank">Documentation
 * from IFC4: IfcMaterialConstituentSet</a>
 * @ingroup OPENLX_MATERIAL
 */

class LX_OPENLXAPP_EXPORT MaterialConstituentSet : public MaterialDefinition, public MaterialSelect
{
    PROXY_HEADER(MaterialConstituentSet, App::MaterialConstituentSet, IFCMATERIALCONSTITUENTSET)

    DECL_PROPERTY(MaterialConstituentSet, Name, Base::String)
    DECL_PROPERTY(MaterialConstituentSet, Description, Base::String)

public:
    ~MaterialConstituentSet();

    std::vector<std::shared_ptr<MaterialConstituent>> getMaterialConstituents() const;
    void setMaterialConstituents(const std::vector<std::shared_ptr<MaterialConstituent>>& aMaterialConstituents);
    void addMaterialConstituent(std::shared_ptr<MaterialConstituent> aMaterialConstituent);
    void removeMaterialConstituent(std::shared_ptr<MaterialConstituent> aMaterialConstituent);

private:
    MaterialConstituentSet() {}
};

}  // namespace OpenLxApp
