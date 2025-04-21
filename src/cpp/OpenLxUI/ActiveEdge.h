///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once
#include <OpenLxApp/Element.h>

#include <Topo/Shape.h>

namespace OpenLxUI
{
/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
struct LX_OPENLXUI_EXPORT ActiveEdge
{
    pConstEdge globalEdge;
    pConstEdge localEdge;
    std::shared_ptr<OpenLxApp::Element> element;
};
}  // namespace OpenLxUI