#pragma once

#include <Geom/Vec.h>
#include <Geom/Pnt.h>
#include <Base/String.h>

namespace Gui
{
    class SceneView;
}
namespace OpenLxUI
{
    /**
     * @brief
     *
     * @ingroup  OPENLX_UI
     * @since    28.0
     */
    class LX_OPENLXUI_EXPORT SceneView
    {
    public:   
        SceneView(void);
        SceneView(const Gui::SceneView& aSceneView);
        ~SceneView(void);

        Base::String getUserName() const;
        void setUserName(const Base::String& aUserName);

        Geom::Pnt getPosition() const;
        void setPosition(const Geom::Pnt& aPosition);
        void updatePosition(const Geom::Pnt& aPosition);
        void getOrientation(Geom::Vec& aAxis, double& aAngle) const;
        void setOrientation(const Geom::Vec& aAxis, double aAngle);
        double getAspectRatio() const;
        void setAspectRatio(double aAspectRatio);
        double getNearDistance() const;
        void setNearDistance(double aNearDistance);
        double getFarDistance() const;
        void setFarDistance(double aFarDistance);
        double getFocalDistance() const;
        void setFocalDistance(double aFocalDistance);
        double getHeight() const;
        void setHeight(double aHeight);
        double getHeightAngle() const;
        void setHeightAngle(double aHeightAngle);
        void setPerspectiveView(bool aOn);
        bool isPerspectiveView() const;
        Geom::Pnt getViewPoint() const;
        void setViewPoint(const Geom::Pnt& aViewPoint);

        void __getInternal__(Gui::SceneView& aSceneView) const;
    private:
        std::shared_ptr<Gui::SceneView> mPimpl;
    };

}  // namespace Gui