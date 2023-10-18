#pragma once

#include <Topo/Types.h>
#include <vector>

namespace App
{
class Element;
}

namespace Topo
{
class RayHit
{
public:
    enum class HitType
    {
        HIT_NONE,
        HIT_VERTEX,
        HIT_EDGE,
        HIT_FACE,
        HIT_ELSE
    };


    RayHit() : hit_element(0), hit_item(nullptr), hit_param(0.), hit_type(), hit_item_idx(-1){};

    RayHit(App::Element* e, pConstTopologicalItem item, double param, Topo::RayHit::HitType h_type, int idx)
        : hit_element(e), hit_item(item), hit_param(param), hit_type(h_type), hit_item_idx(idx){};

    App::Element* getHitElement() { return hit_element; };
    pConstTopologicalItem getHitItem() { return hit_item; };
    double getHitParam() { return hit_param; };
    RayHit::HitType getHitType() { return hit_type; };
    int getHitItemIdx() { return hit_item_idx; };

private:
    App::Element* hit_element;
    pConstTopologicalItem hit_item;
    int hit_item_idx;
    double hit_param;
    Topo::RayHit::HitType hit_type = Topo::RayHit::HitType::HIT_NONE;
};

typedef std::vector<RayHit> RayHitVector;
}  // namespace Topo