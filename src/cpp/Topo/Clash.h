#pragma once

namespace Topo
{
enum class BodyClashType  // http://doc.spatial.com/qref/ACIS/html/group__INTRAPICLASH.html#gc83919c84495436a3960bc65d1e67083
{
    CLASH_UNKNOWN,
    CLASH_NONE,
    CLASH_UNCLASSIFIED,
    CLASH_CONTAINED,
    CLASH_CONTAINED_ABUTS,
    CLASH_ABUTS,
    CLASH_COINCIDENT,
    CLASH_INTERLOCK
};

enum class ClashMode  // http://doc.spatial.com/qref/ACIS/html/group__INTRAPICLASH.html#g84fecb80099bf036f1df154427f6a1d5
{
    CLASH_EXISTENCE_ONLY,
    CLASH_CLASSIFY_BODIES,
    CLASH_CLASSIFY_SUB_ENTITIES
};

enum class FaceClashType  // entity_clash_type
{
    CLASH_UNKNOWN,
    CLASH_NONE,
    CLASH_UNCLASSIFIED,
    CLASH_COI_INSIDE,
    CLASH_COI_OUTSIDE,
    CLASH_AINB,
    CLASH_BINA,
    CLASH_TOUCH,
    CLASH_INTERLOCK
};
}  // namespace Topo
