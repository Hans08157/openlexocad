#pragma once

#include <Base/String.h>

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT CdwkAttributeData
{
public:
    Base::String buildingGroup = L"";
    Base::String buildingSubGroup = L"";
    Base::String comment = L"";
    Base::String sku = L"";  // stock-keeping-unit
    Base::String usertext_1 = L"";
    Base::String usertext_2 = L"";
    Base::String usertext_3 = L"";
    Base::String usertext_4 = L"";
    Base::String usertext_5 = L"";
    Base::String usertext_6 = L"";
    Base::String usertext_7 = L"";
    Base::String usertext_8 = L"";
    Base::String usertext_9 = L"";
    Base::String usertext_10 = L"";
    int production_nb = 0;


    ~CdwkAttributeData() {}
    CdwkAttributeData();
};
}  // namespace OpenLxApp
