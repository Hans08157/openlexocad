#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Member)

namespace OpenLxApp
{
/**
 * @brief A Member is a structural member designed to carry loads between or beyond points of support.
 * It is not required to be load bearing. The orientation of the member (being horizontal, vertical or sloped)
 * is not relevant to its definition (in contrary to Beam and Column). An IMember represents a
 * linear structural element from an architectural or structural modeling point of view and shall be used
 * if it cannot be expressed more specifically as either an Beam or an Column.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcmember.htm" target="_blank">Documentation from IFC4: IfcMember</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Member : public Element
{
    PROXY_HEADER(Member, App::Member, IFCMEMBER)

public:
    virtual ~Member(void);

    enum class MemberTypeEnum
    {
        BRACE,
        CHORD,
        COLLAR,
        MEMBER,
        MULLION,
        PLATE,
        POST,
        PURLIN,
        RAFTER,
        STRINGER,
        STRUT,
        STUD,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(MemberTypeEnum aType);
    MemberTypeEnum getPredefinedType() const;

protected:
    Member() {}
};

}  // namespace OpenLxApp