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

#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/Product.h>
#include <OpenLxApp/Root.h>
#include <OpenLxUI/CurveDesigner.h>



namespace OpenLxUI
{
class CurveDesignerP;

/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    26.0
 */
class LX_OPENLXUI_EXPORT CurveDesigner
{
public:
    CurveDesigner();

private:
    std::shared_ptr<OpenLxUI::CurveDesignerP> mPimpl;
};
}  // namespace OpenLxUI