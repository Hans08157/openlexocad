#pragma once

#include <Geom/Pln.h>
#include <OpenLxApp/CurveBoundedPlane.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/FaceBasedSurfaceModel.h>
#include <Topo/Shape.h>

#include <memory>

/** @defgroup OPENLX_SURFACE_API Surface API
 */

namespace OpenLxApp
{
LX_OPENLXAPP_EXPORT std::shared_ptr<CurveBoundedPlane> createRectangularTrimmedPlane(std::shared_ptr<Document> aDoc,
                                                                                  const Geom::Pln& aPln,
                                                                                  double aWidth,
                                                                                  double aHeight);
LX_OPENLXAPP_EXPORT std::shared_ptr<CurveBoundedPlane> createCurveBoundedPlaneFromFace(std::shared_ptr<Document> aDoc, pConstFace aFace);
LX_OPENLXAPP_EXPORT std::shared_ptr<FaceBasedSurfaceModel> createFaceBasedSurfaceModel(std::shared_ptr<Document> aDoc, pConstMesh aMesh);


}  // namespace OpenLxApp