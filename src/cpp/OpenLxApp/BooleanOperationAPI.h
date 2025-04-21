#pragma once


#include <Geom/Pln.h>
#include <OpenLxApp/Element.h>

#include <vector>

/** @defgroup OPENLX_BOP_API Boolean Operation API
 */

namespace OpenLxApp
{
LX_OPENLXAPP_EXPORT ErrorCode bop_cut(std::shared_ptr<Element> softElem,
                                   std::shared_ptr<Element> hardElem,
                                   std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_cut(std::shared_ptr<Element> softElem,
                                   const std::vector<std::shared_ptr<Element>>& hardElems,
                                   std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_cut(std::shared_ptr<Element> softElem,
                                   std::shared_ptr<Element>* hardElems,
                                   int hardElemsSize,
                                   std::shared_ptr<Element>* result,
                                   int resultSize,
                                   int& nbElementsInResult);
LX_OPENLXAPP_EXPORT ErrorCode bop_common(std::shared_ptr<Element> firstElem,
                                      std::shared_ptr<Element> secondElem,
                                      std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_cutWithPlane(std::shared_ptr<Element> elem, const Geom::Pln& plane, std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_splitByPlane(std::shared_ptr<Element> elem, const Geom::Pln& plane, std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_sectionWithPlane(std::shared_ptr<Element> elem, const Geom::Pln& plane, std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_section(std::shared_ptr<Element> firstElem,
                                       std::shared_ptr<Element> secondElem,
                                       std::vector<std::shared_ptr<Element>>& result);
LX_OPENLXAPP_EXPORT ErrorCode bop_fuse(const std::vector<std::shared_ptr<Element>>& elems, std::shared_ptr<Element>& result);

/// @cond INTERNAL
LX_OPENLXAPP_EXPORT void bop_startTimer();
LX_OPENLXAPP_EXPORT int bop_stopTimer();
LX_OPENLXAPP_EXPORT int bop_elapsedTime();
/// @endcond
}  // namespace OpenLxApp
