#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Formwork)

namespace OpenLxApp
{


class LX_OPENLXAPP_EXPORT Formwork : public Element
{
    PROXY_HEADER(Formwork, App::Formwork, IFC_ENTITY_UNDEFINED)

public:
    enum class FormworkTypeEnum
    {
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(FormworkTypeEnum aType);
    FormworkTypeEnum getPredefinedType() const;

    virtual ~Formwork(void);


protected:
    Formwork() {}
};

}  // namespace OpenLxApp