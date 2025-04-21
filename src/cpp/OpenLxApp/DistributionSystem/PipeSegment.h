#pragma once

#include <OpenLxApp/DistributionSystem/FlowSegment.h>

FORWARD_DECL(App, PipeSegment)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT PipeSegment : public FlowSegment
{
    PROXY_HEADER(PipeSegment, App::PipeSegment, IFCPIPESEGMENT)

public:
    enum class PipeSegmentTypeEnum
    {
        CULVERT,
        FLEXIBLESEGMENT,
        RIGIDSEGMENT,
        GUTTER,
        SPOOL,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(PipeSegmentTypeEnum aType);
    PipeSegmentTypeEnum getPredefinedType() const;

    ~PipeSegment() override = default;

protected:
    PipeSegment() {}
};
}
