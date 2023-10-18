#pragma once

#include <Base/GlobalId.h>
#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Globals.h>

FORWARD_DECL(App, Root)

namespace OpenLxApp
{
class Document;

/**
 * @brief Root is the base class of all BIM related entities.
 * All BIM entities can be identified by a Globally Unique Id.
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT Root : public DocObject
{
    PROXY_HEADER_ABSTRACT(Root, App::Root, IFCROOT)

public:
    /** @name Identification */
    //@{
    Base::GlobalId getGlobalId() const;
    bool setGlobalId(const Base::GlobalId& aGlobalId);
    //@}

    void setUserName(const Base::String& aName);
    Base::String getUserName() const;

    virtual ~Root(void);

protected:
    Root() {}
};
}  // namespace OpenLxApp