#pragma once

#include <OpenLxApp/ParameterizedProfileDef.h>



FORWARD_DECL(Part, IShapeProfileDef)

namespace OpenLxApp
{
/*!
 * @brief IShapeProfileDef defines a section profile that provides the
 * defining parameters of an 'I' or 'H' section. The I-shape profile has
 * values for its overall depth, width and its web and flange thicknesses.
 * Additionally a fillet radius, flange edge radius, and flange slope may be given.
 * This profile definition represents an I-section which is symmetrical
 * about its major and minor axes; top and bottom flanges are equal and centred on the web.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcishapeprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcIShapeProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT IShapeProfileDef : public ParameterizedProfileDef
{
    PROXY_HEADER(IShapeProfileDef, Part::IShapeProfileDef, IFCISHAPEPROFILEDEF)

    DECL_PROPERTY(IShapeProfileDef, OverallWidth, double)
    DECL_PROPERTY(IShapeProfileDef, OverallDepth, double)
    DECL_PROPERTY(IShapeProfileDef, WebThickness, double)
    DECL_PROPERTY(IShapeProfileDef, FlangeThickness, double)
    DECL_PROPERTY(IShapeProfileDef, FilletRadius, double)
    // DECL_PROPERTY(IShapeProfileDef, FlangeEdgeRadius, double)
    // DECL_PROPERTY(IShapeProfileDef, FlangeSlope, double)

public:
    static std::vector<Base::String> getPredefinedSteelProfileTypes();
    static std::vector<Base::String> getPredefinedSteelProfiles(const Base::String& aTypeName);

    bool setValuesFromPredefinedSteelProfile(const Base::String& aProfileName);
    virtual ~IShapeProfileDef(void);

protected:
    IShapeProfileDef(void) {}
};
}  // namespace OpenLxApp