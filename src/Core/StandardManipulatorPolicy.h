#pragma once 

#include <Geom/Dir.h>

namespace Core
{
struct LX_CORE_EXPORT StandardManipulatorPolicy
{
    enum Flags
    {
        SHOWBBOX = 1 << 0,
        SHOWSCALER = 1 << 1,
        SHOWONLYXSCALER = 1 << 2,
        SHOWONLYZSCALER = 1 << 3,
        SHOWCORNERSCALER = 1 << 4,
        SHOWSCALERIFBBOXISHIDDEN = 1 << 5,
        SHOWCORNERSCALERIFBBOXISHIDDEN = 1 << 6,
        SHOWTRANSLATIONPLANE = 1 << 7,
        HASOWNTRANSLATIONPLANE = 1 << 8,
        TRANSLATEXENABLED = 1 << 9,
        TRANSLATEYENABLED = 1 << 10,
        TRANSLATEZENABLEDL = 1 << 11,
        TRANSLATEZENABLEDW = 1 << 12,
        TRANSLATEZENABLEDH = 1 << 13,
        HIGHLIGHT = 1 << 14,
        ENABLECORNERTABSNONUNIFORMSCALE = 1 << 15,
        SHOWTRANSLATEZIFBBOXISHIDDEN = 1 << 16,
        SHOWONLYXZSCALER = 1 << 17,
        NEVERSHOWBBOX = 1 << 18
    };

    bool showBBox = true;
    bool showScaler = true;
    bool showOnlyXScaler = false;
    bool showOnlyZScaler = false;
    bool showOnlyXZScaler = false;
    bool showCornerScaler = false;
    bool showScalerIfBBoxIsHidden = false;
    bool showCornerScalerIfBBoxIsHidden = false;
    bool showTranslationPlane = false;
    bool hasOwnTranslationPlane = false;
    bool translateXEnabled = true;
    bool translateYEnabled = true;
    bool translateZEnabledL = true;
    bool translateZEnabledW = true;
    bool translateZEnabledH = true;
    bool showtranslateZIfBBoxIsHidden = false;
    bool highlight = true;
    bool enableCornerTabsNonUniformScale = false;
    Geom::Dir OwnTranslationPlane;
    bool draggerSpecialForClippingBox = false;
    bool newerShowBBox = false;

    bool isGeoPolicy = false; // DG, no need to save, only for debugging.

    static StandardManipulatorPolicy getFromUInt64(uint64_t aValue)
    {
        StandardManipulatorPolicy policy;
        policy.showBBox = (aValue & Core::StandardManipulatorPolicy::SHOWBBOX);
        policy.showScaler = (aValue & Core::StandardManipulatorPolicy::SHOWSCALER);
        policy.showOnlyXScaler = (aValue & Core::StandardManipulatorPolicy::SHOWONLYXSCALER);
        policy.showOnlyZScaler = (aValue & Core::StandardManipulatorPolicy::SHOWONLYZSCALER);
        policy.showOnlyXZScaler = (aValue & Core::StandardManipulatorPolicy::SHOWONLYXZSCALER);
        policy.showCornerScaler = (aValue & Core::StandardManipulatorPolicy::SHOWCORNERSCALER);
        policy.showScalerIfBBoxIsHidden = (aValue & Core::StandardManipulatorPolicy::SHOWSCALERIFBBOXISHIDDEN);
        policy.showCornerScalerIfBBoxIsHidden = (aValue & Core::StandardManipulatorPolicy::SHOWCORNERSCALERIFBBOXISHIDDEN);
        policy.showTranslationPlane = (aValue & Core::StandardManipulatorPolicy::SHOWTRANSLATIONPLANE);
        policy.hasOwnTranslationPlane = (aValue & Core::StandardManipulatorPolicy::HASOWNTRANSLATIONPLANE);
        policy.translateXEnabled = (aValue & Core::StandardManipulatorPolicy::TRANSLATEXENABLED);
        policy.translateYEnabled = (aValue & Core::StandardManipulatorPolicy::TRANSLATEYENABLED);
        policy.translateZEnabledL = (aValue & Core::StandardManipulatorPolicy::TRANSLATEZENABLEDL);
        policy.translateZEnabledW = (aValue & Core::StandardManipulatorPolicy::TRANSLATEZENABLEDW);
        policy.translateZEnabledH = (aValue & Core::StandardManipulatorPolicy::TRANSLATEZENABLEDH);
        policy.highlight = (aValue & Core::StandardManipulatorPolicy::HIGHLIGHT);
        policy.enableCornerTabsNonUniformScale = (aValue & Core::StandardManipulatorPolicy::ENABLECORNERTABSNONUNIFORMSCALE);
        policy.showtranslateZIfBBoxIsHidden = (aValue & Core::StandardManipulatorPolicy::SHOWTRANSLATEZIFBBOXISHIDDEN);
        return policy;
    }


   

};

}  // namespace Core