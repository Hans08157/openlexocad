#pragma once

#include <Geom/Pnt2d.h>
#include <OpenLxApp/ArbitraryClosedProfileDef.h>
#include <OpenLxApp/ArbitraryOpenProfileDef.h>
#include <OpenLxApp/ArbitraryProfileDefWithVoids.h>
#include <OpenLxApp/CurveBoundedPlane.h>
#include <OpenLxApp/Document.h>

#include <memory>

/** @defgroup OPENLX_PROFILE_API Profile API
 */

namespace OpenLxApp
{
LX_OPENLXAPP_EXPORT void setShapeProfileParams(std::shared_ptr<Element> aElem, const Base::String& aProfileName);
LX_OPENLXAPP_EXPORT std::shared_ptr<ArbitraryClosedProfileDef> createArbitraryClosedProfileDef(std::shared_ptr<Document> aDoc,
                                                                                            const std::vector<Geom::Pnt2d> aOuterLoop);
LX_OPENLXAPP_EXPORT std::shared_ptr<ArbitraryOpenProfileDef> createArbitraryOpenProfileDef(std::shared_ptr<Document> aDoc,
                                                                                        const std::vector<Geom::Pnt2d> aLoop);
LX_OPENLXAPP_EXPORT std::shared_ptr<ArbitraryProfileDefWithVoids> createArbitraryProfileDefWithVoids(
    std::shared_ptr<Document> aDoc,
    const std::vector<Geom::Pnt2d> aOuterLoop,
    const std::vector<std::vector<Geom::Pnt2d>> aInnerLoops);


}  // namespace OpenLxApp