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

namespace App
{
class Group;
}

namespace OpenLxApp
{
/**
 * @brief A class to group Elements.
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT Group : public DocObject
{
    PROXY_HEADER(Group, App::Group, IFCGROUP)
public:
    friend class Document;

    void addElement(std::shared_ptr<Element> aElem);
    void addGroup(std::shared_ptr<Group> aGroupChild);
    void removeElement(std::shared_ptr<Element> aElem);
    void removeGroup(std::shared_ptr<Group> aGroupChild);
    std::shared_ptr<Group> getTopGroup() const;
    std::shared_ptr<Group> getParentGroup() const;
    std::vector<std::shared_ptr<Element>> getAllElements() const;
    std::vector<std::shared_ptr<Group>> getChildren() const;
    virtual ~Group(void);

private:
    Group() {}
};

}  // namespace OpenLxApp
