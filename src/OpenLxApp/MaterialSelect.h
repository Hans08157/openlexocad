#pragma once

namespace OpenLxApp
{
/*!
 *
 * @brief MaterialSelect provides selection of either a material definition or a material usage definition that can be assigned
 * to an element, a resource or another entity within this specification.
 *
 * MaterialDefinition
 *	Material
 *	MaterialLayer
 *	MaterialLayerSet
 *	MaterialProfile
 *	MaterialProfileSet
 *	MaterialConstituent
 *	MaterialConstituentSet
 *
 * MaterialUsageDefinition
 *	MaterialLayerSetUsage
 *	MaterialProfileSetUsage
 *
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcmaterialselect.htm" target="_blank">Documentation from
 *IFC4: IfcMaterialSelect</a>
 * @ingroup OPENLX_MATERIAL
 */

class LX_OPENLXAPP_EXPORT MaterialSelect
{
public:
    MaterialSelect();
    virtual ~MaterialSelect();
};

}  // namespace OpenLxApp
