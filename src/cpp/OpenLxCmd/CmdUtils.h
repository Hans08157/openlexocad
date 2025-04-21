#pragma once

#include <App/Element.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/SubElement.h>

#include <memory>
#include <vector>


namespace OpenLxCmd
{
std::vector<App::Element*> toAppElements(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
std::vector<std::shared_ptr<OpenLxApp::Element>> toOpenLxElements(const std::vector<App::Element*>& aElems);
std::shared_ptr<OpenLxApp::Element> toOpenLxElement(App::Element* aElem);
std::shared_ptr<OpenLxApp::SubElement> toOpenLxSubElement(App::SubElement* aElem);
}  // namespace OpenLxCmd