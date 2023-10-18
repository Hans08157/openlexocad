#pragma once

#include <Geom/Pnt.h>
#include <OpenLxApp/CompositeCurve.h>
#include <OpenLxApp/CompositeCurveSegment.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Polyline.h>
#include <OpenLxApp/TrimmedCurve.h>

#include <memory>

/** @defgroup OPENLX_CURVE_API Curve API
 */

namespace OpenLxApp
{
LX_OPENLXAPP_EXPORT std::shared_ptr<CompositeCurveSegment> createLineSegment(std::shared_ptr<Document> aDoc,
                                                                          const Geom::Pnt& fromPnt,
                                                                          const Geom::Pnt& toPnt);
LX_OPENLXAPP_EXPORT std::shared_ptr<CompositeCurveSegment> createArc3PointsSegment(std::shared_ptr<Document> aDoc,
                                                                                const Geom::Pnt& startPnt,
                                                                                const Geom::Pnt& passagePnt,
                                                                                const Geom::Pnt& endPnt);
LX_OPENLXAPP_EXPORT std::shared_ptr<CompositeCurveSegment> createTangentArcSegment(std::shared_ptr<Document> aDoc,
                                                                                std::shared_ptr<CompositeCurveSegment> lastSegment,
                                                                                const Geom::Pnt& pnt);

LX_OPENLXAPP_EXPORT std::shared_ptr<TrimmedCurve> createStraight(std::shared_ptr<Document> aDoc, const Geom::Pnt& fromPnt, const Geom::Pnt& toPnt);
LX_OPENLXAPP_EXPORT std::shared_ptr<TrimmedCurve> createArc3Points(std::shared_ptr<Document> aDoc,
                                                                const Geom::Pnt& startPnt,
                                                                const Geom::Pnt& passagePnt,
                                                                const Geom::Pnt& endPnt);
LX_OPENLXAPP_EXPORT std::shared_ptr<TrimmedCurve> createTangentArc(std::shared_ptr<Document> aDoc,
                                                                std::shared_ptr<BoundedCurve> lastCurve,
                                                                const Geom::Pnt& endPnt);

LX_OPENLXAPP_EXPORT std::shared_ptr<Curve> createOffsetCurveFromWire(std::shared_ptr<Document> aDoc,
                                                                  pConstWire wire,
                                                                  const Geom::Dir& refDirection,
                                                                  double offset);
LX_OPENLXAPP_EXPORT std::shared_ptr<CompositeCurve> createCompositeCurveFromWire(std::shared_ptr<Document> aDoc, pConstWire wire);
LX_OPENLXAPP_EXPORT std::shared_ptr<Polyline> createPolylineFromWire(std::shared_ptr<Document> aDoc, pConstWire wire);
LX_OPENLXAPP_EXPORT std::shared_ptr<BoundedCurve> createBoundedCurveFromEdge(std::shared_ptr<Document> aDoc, pConstEdge edge);

/// Creates an edges from intersecting surfaces which are determined  by the wire and angle. Returns false if creation fails.
// LX_OPENLXAPP_EXPORT bool createPyramidEdgesFromWire(Core::CoreDocument* doc, pConstWire wire, const Geom::Dir& refDirection, const std::vector<double>&
// slopes, std::vector<Part::Curve*>& edges);
/// Creates a Clothoid from an Edge. Returns Null if creation fails.
// LX_OPENLXAPP_EXPORT std::shared_ptr<Clothoid> createClothoidFromEdge(Core::CoreDocument* doc, pConstEdge edge);
/// Creates a BSplineCurve from a Wire. Returns Null if creation fails.
// LX_OPENLXAPP_EXPORT std::shared_ptr<BSplineCurve> createBSplineCurveFromWire(Core::CoreDocument* doc, pConstWire wire);

}  // namespace OpenLxApp