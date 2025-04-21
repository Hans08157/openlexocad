#pragma once

// HPK: Intentionally put in separate file to avoid
// conflict with mainpage in App.Application

/**
 * @mainpage OpenLexocad API Reference
 *
 * @section intro_sec Introduction
 *
 * OpenLexocad is the public API to the Lexocad application.
 * Lexocad is a hybrid parametric 3d modeler made for
 * Building Information Modeling (BIM).<br>
 * Lexocad is part of the cadwork software family <a href="http://www.cadwork.com" target="_blank">(www.cadwork.com)</a>.
 *
 * @section install_sec Installation
 * You can download Lexocad at <a href="http://www.lexocad.com" target="_blank">www.lexocad.com</a>.
 * You can download the Lexocad public API called OpenLexocad
 * at <a href="http://www.openlexocad.com" target="_blank">www.openlexocad.com</a>.
 *
 * @subsection Modules
 * At present OpenLexocad consists of eight modules:
 * - Base : Basic types.
 *    - @ref Base::String
 *    - @ref Base::Color
 *    - @ref Base::GlobalId
 * - Core : Core Application Services
 *    - @ref Core::Command
 * - Geom : Basic non-persistent geometry types
 *    - @ref Geom::Vec
 *    - @ref Geom::Pnt
 *    - @ref Geom::Dir
 *    - @ref Geom::Ax2
 *    - @ref Geom::Trsf
 *    - @ref Geom::GeomTools
 * - Draw : Basic types for rendering
 *    - @ref Draw::OglMaterial
 *    - @ref Draw::DrawStyle
 * - Topo : Topological types and services
 *    - @ref TOPO_SHAPES
 *    - @ref TOPO_SHAPETOOLS
 * - OpenLxApp : API for all persistent application data types
 *    - @ref OPENLX_FRAMEWORK
 *    - @ref OPENLX_BUILDINGELEMENTS
 *    - @ref OPENLX_SPATIALELEMENTS
 *    - @ref OPENLX_MATERIAL
 *    - @ref OPENLX_GEOMETRIC_ITEMS
 *    - @ref OPENLX_PROFILEDEF
 *    - @ref OPENLX_PROFILE_API
 *    - @ref OPENLX_CURVE_API
 *    - @ref OPENLX_SURFACE_API
 *    - @ref OPENLX_SOLID_API
 *    - @ref OPENLX_BOP_API
 *    - @ref OPENLX_EXPORTER
 *    - @ref OPENLX_IMPORTER
 * - OpenLxUI  : API for the Lexocad user interface
 *    - @ref OpenLxUI::UIDocument
 *    - @ref OpenLxUI::Selection
 * - OpenLxCmd : API for Lexocad commands
 *
 */