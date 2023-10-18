
/**
 * @file
 * AbstractBehaviorMode class header.
 *
 */
#pragma once 

#include <Base/Base.h>
#include <Base/Observer.h>
#include <Core/EventInterface.h>


namespace Core
{
class ServiceInterface;
class GUIInterface;
class ViewMgrInterface;
class BehaviorModeNotification;

typedef std::map<std::string, bool> BehaviorAttributeMap;


/**
 * This is just an interface for the behavior modes of the Executor module.
 *
 */
class LX_CORE_EXPORT AbstractBehaviorMode : public Base::BaseClass, public Base::Subject<BehaviorModeNotification>
{
    TYPESYSTEM_HEADER();

protected:
    AbstractBehaviorMode();

public:
    virtual ~AbstractBehaviorMode(void);
    void setInterfaces(ViewMgrInterface* vi, GUIInterface* gi, ServiceInterface* si);
    void setViewInterface(ViewMgrInterface* vi);
    void setGuiInterface(GUIInterface* gi);
    void setServiceInterface(ServiceInterface* si);

    virtual void keyPress(const KeyEvent& event);
    virtual void keyRelease(const KeyEvent& event);
    virtual void wheel(const MWheelEvent& event);
    virtual void mouseMove(const MouseEvent& event);
    virtual void mousePress(const MouseEvent& event);
    virtual void mouseRelease(const MouseEvent& event);
    virtual void mouseEnter(void);
    virtual void mouseLeave(void);
    virtual void resize(const ResizeEvent& event);

    virtual void reset(void) = 0;
    virtual void initialProcedure(void) = 0;
    virtual void finalProcedure(void) = 0;

    virtual void setTextInput(const std::string& input);
    virtual void setAttributes(const BehaviorAttributeMap& attributes);

    virtual const char* subject_name(void) { return "AbstractBehaviorMode"; };



protected:
    ViewMgrInterface* _view_i;
    GUIInterface* _gui_i;
    ServiceInterface* _service_i;


    int _old_mouse_x;
    int _old_mouse_y;


    void defaultEnd(void);
};



/**
 *
 *
 */
class LX_CORE_EXPORT AbstractBehaviorSubMode
{
public:
    AbstractBehaviorSubMode(void);
    virtual ~AbstractBehaviorSubMode(void);

    virtual void keyPress(const KeyEvent& event);
    virtual void wheel(const MWheelEvent& event);
    virtual void mouseMove(const MouseEvent& event);
    virtual void mousePress(const MouseEvent& event);
    virtual void mouseRelease(const MouseEvent& event);
    virtual void mouseEnter(void);
    virtual void mouseLeave(void);

    virtual void setTextInput(const std::string& input);
    virtual int getId(void) const = 0;
};



/**
 *
 */
class LX_CORE_EXPORT BehaviorModeNotification
{
public:
    enum Reason
    {
        BEHAVIOR_MODE_ENDS,
        BLOCK_MOUSE_REQUEST,
        UNBLOCK_MOUSE_REQUEST
    };

    Reason _why;
};



/**
 *
 *
 */
class LX_CORE_EXPORT BehaviorModeFactory
{
public:
    BehaviorModeFactory(void);
    ~BehaviorModeFactory(void);

    virtual AbstractBehaviorMode* createByFactory(ViewMgrInterface* vi, GUIInterface* gi, ServiceInterface* si) = 0;

    static std::map<std::string, BehaviorModeFactory*> _registry;
    static bool registerFactory(const std::string& name, BehaviorModeFactory* fact);

    static AbstractBehaviorMode* create(ViewMgrInterface* vi, GUIInterface* gi, ServiceInterface* si, const std::string& type);
};



}  // namespace Core



#define ADD_BEHAVIORMODE_FACTORY(_factoryName_, _class_) \
    class _factoryName_ : public Core::BehaviorModeFactory \
    { \
    private: \
        virtual Core::AbstractBehaviorMode* createByFactory(Core::ViewMgrInterface* vi, Core::GUIInterface* gi, Core::ServiceInterface* si) \
        { \
            Core::AbstractBehaviorMode* o = new _class_; \
            o->setInterfaces(vi, gi, si); \
            return o; \
        } \
    };


#define REGISTER_BEHAVIORMODE_FACTORY(_factoryName_, _class_) \
    Core::BehaviorModeFactory::_registry[#_class_] = (Core::BehaviorModeFactory*)new _factoryName_();


