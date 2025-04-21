#pragma once
#include <Base/Timer.h>
#include <Base/Log.h>
#include <sstream>

namespace Base
{
template <class _MessageType>
class Subject;

/** Observer class
 *  Implementation of the well known Observer Design Pattern.
 *  The observed object, which inherit FCSubject, will call all
 *  its observers in case of changes. A observer class has to
 *  Attach itself to the observed object.
 *  @see FCSubject
 */
template <class _MessageType>
class Observer
{
public:
    /**
     * A constructor.
     * No special function so far.
     */
    Observer(int observerPriority = 1)
        : _observerPriority(observerPriority)
        {

        };

    /**
     * A destructor.
     * No special function so far.
     */
    virtual ~Observer()
    {
        cDebug("~Observer %s %x", this->name() ? this->name() : "No Name", this);
        if (!_subjects.empty())
        {
            auto copy_subjects = _subjects;
            cWarn("Observer %s %x is not detached!!!!", this->name() ? this->name() : "No Name", this);
            for (auto s : copy_subjects)
                s->detach(this);
        }
        __deadVal = 0xDEADBEEF;
    };



    /**
     * This method need to be reimplemented from the concrete Observer
     * and get called by the observed class
     * @param pCaller a reference to the calling object
     */
    virtual void onChange(Subject<_MessageType>* rCaller, _MessageType rcReason) = 0;

    /**
     * This method need to be reimplemented from the concrete Observer
     * and get called by the observed class
     * @param pCaller a reference to the calling object
     */
    virtual void onDestroy(Subject<_MessageType>& /*rCaller*/) {}

    /**
     * This method can be reimplemented from the concrete Observer
     * and returns the name of the observer. Needed to use the Get
     * method of the Subject.
     */
    virtual const char* name(void) { return "<no name>"; }

    /**
     * Observers with higher priority will be called first. Default priority is 1.
     */
    inline int getObserverPriority() const { return _observerPriority; }

    void setAttached(Subject<_MessageType>* t)
    {
        auto it = std::find(_subjects.begin(), _subjects.end(), t);
        if (it == _subjects.end())
            _subjects.push_back(t);
        else
            cWarn("Observer is already attached.");
    };
    void setDetached(Subject<_MessageType>* t)
    {
        auto it = std::find(_subjects.begin(), _subjects.end(), t);
        if (it != _subjects.end())
            _subjects.erase(it);
        else
            cWarn("Observer is already detached.");
        //_subjects.erase(std::remove(_subjects.begin(), _subjects.end(), t),_subjects.end());
    };

    long __deadVal = 0xBADEAFFE;
private:    

    std::vector<Subject<_MessageType>*> _subjects;
    int _observerPriority;
};


/** Subject class
 *  Implementation of the well known Observer Design Pattern.
 *  The observed object, which inherit FCSubject, will call all
 *  its observers in case of changes. A observer class has to
 *  Attach itself to the observed object.
 *  @see FCObserver
 */
template <class _MessageType>
class Subject
{
public:
    typedef Observer<_MessageType> ObserverType;
    typedef _MessageType MessageType;
    typedef Subject<_MessageType> SubjectType;

    struct ObserverHolder
    {
        ObserverHolder() = default;
        ObserverHolder(ObserverType* aobserverPtr)
            : observerPtr(aobserverPtr), observerPriority(aobserverPtr->getObserverPriority()), isAttached(true) /*, isDeleted(false)*/
        {
        }
        ObserverType*  observerPtr;
        int            observerPriority;    
        mutable bool   isAttached;
        //mutable bool   isDeleted;
    };

    

    /**
     * A constructor.
     * No special function so far.
     */
    Subject() : _running_notify{false} { };

    /**
     * A destructor.
     * No special function so far.
     */
    virtual ~Subject()
    {        

        if( _running_notify )
        {
            cWarn("FATAL ERROR, ~Subject %X call while running notify!" ); 
            cDebuggerBreak("FATAL ERROR ~Subject call running notify!");
        }
        
        if (!_ObserverSet.empty())
        {
            cWarn("Not detached all observers yet" );
        }
    }

    /** Attach an Observer
     * Attach an Observer to the list of Observers which get
     * called when Notify is called.
     * @param ToObserv A pointer to a concrete Observer
     * @see Notify
     */
    void attach(Observer<_MessageType>* ToObserv)
    {
        if( ToObserv->__deadVal != 0xBADEAFFE )
        {
            cWarn("Subject try to attach a deleted Observer");
            return;
        }
        
        ToObserv->setAttached(this);

        std::string name = ToObserv->name() ? ToObserv->name() : "No Name";
        std::ostringstream oss;
        oss << " " << ToObserv;
        name += oss.str();

        if( _running_notify )
        {
            if (_ObserverSet_AddedLaterCopy.find(ToObserv) != _ObserverSet_AddedLaterCopy.end())
            {
                cWarn("Subject %x, attach Observer %s %X while running notify already attached", this,
                      ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
            }
            else
            {
                auto ret = _ObserverSet_AddedLater.insert(ObserverHolder(ToObserv));
                if (ret.second)
                {
                    cDebug("Subject %x, attach Observer %s %X while running notify", this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
                }
                else
                {
                    cWarn("Subject %x, attach Observer %s %X while running notify already attached", this,
                          ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
                }
            }
        }
        else
        {
            auto ret = _ObserverSet.insert(ObserverHolder(ToObserv));            
            if(ret.second)
            {
                cDebug("Subject %x, attach Observer %s %X ",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
            }
            else
            {
                cWarn("Subject %x, attach Observer %s %X already attached",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
            }
        }

        
    }

    /** Detach an Observer
     * Detach an Observer from the list of Observers which get
     * called when Notify is called.
     * @param ToObserv A pointer to a concrete Observer
     * @see Notify
     */
    void detach(Observer<_MessageType>* ToObserv)
    {      
        cDebug("DETACH 0x%X",ToObserv);
        ToObserv->setDetached(this);
        if( _running_notify )
        {
            auto it = _ObserverSet.find(ObserverHolder(ToObserv));            
            if( it != _ObserverSet.end() )
            {
                cWarn("**** Subject %x, detach Observer %s %X while running notify",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
                (*it).isAttached = false;
            }

            auto it2 = _ObserverSet_AddedLater.find(ObserverHolder(ToObserv));
            if( it2 != _ObserverSet_AddedLater.end() )
            {
                cWarn("**** Subject %x, detach Observer %s %X while running notify",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
                (*it2).isAttached = false;
            }

            auto it3 = _ObserverSet_AddedLaterCopy.find(ObserverHolder(ToObserv));
            if (it3 != _ObserverSet_AddedLaterCopy.end())
            {
                cWarn("**** Subject %x, detach Observer %s %X while running notify", this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
                (*it2).isAttached = false;
            }

        }
        else
        {
            if (_ObserverSet.find(ToObserv) != _ObserverSet.end())
            {
                cDebug("Subject %x, detach Observer %s %X",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
                _ObserverSet.erase(ToObserv);
            }
            else
            {
                cWarn("Subject %x, detach Observer %s %X not found",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
            }        
        }
        
    }

    //void observerDeleted(Observer<_MessageType>* ToObserv)
    //{
    //    auto it = _ObserverSet.find(ObserverHolder(ToObserv));            
    //    if( it != _ObserverSet.end() )
    //    {
    //            cWarn("**** Subject %x, detach Observer %s %X while running notify",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
    //            (*it).isDeleted = true;
    //    }
    //    auto it2 = _ObserverSet_AddedLater.find(ObserverHolder(ToObserv));
    //    if( it2 != _ObserverSet_AddedLater.end() )
    //    {
    //            cWarn("**** Subject %x, detach Observer %s %X while running notify",this, ToObserv->name() ? ToObserv->name() : "No Name", ToObserv);
    //            (*it2).isDeleted = true;
    //    }
    //
    //}

    /** Clears the list of all registered observers.
     * @note Using this function in your code may be an indication of design problems.
     */
    void detachAll()
    {
        if (_running_notify)
            _allDetachedWhileRunningNotify = true;

        for (const auto& observer : _ObserverSet)
        {
            if( observer.isAttached )
                observer.observerPtr->setDetached(this);
        }

        for (const auto& observer : _ObserverSet_AddedLater)
        {
            if( observer.isAttached )
                observer.observerPtr->setDetached(this);
        }

        for (const auto& observer : _ObserverSet_AddedLaterCopy)
        {
            if (observer.isAttached)
                observer.observerPtr->setDetached(this);
        }

        _ObserverSet.clear();
        _ObserverSet_AddedLater.clear();
        _ObserverSet_AddedLaterCopy.clear();
    }

    /** Notify all Observers
     * Send a message to all Observers attached to this subject.
     * The Message depends on the implementation of a concrete
     * Observer and Subject.
     * @see Notify
     */

    void notify_internal(_MessageType& rcReason, size_t deep)
    {
        if( deep > 10 )
        {
            cWarn("ERROR notify_internal, to deep recursion!");
            cDebuggerBreak("ERROR notify_internal, to deep recursion!");
            return;
        }

        for (const auto& observer : _ObserverSet)
        {
        	// Was detached, maybe in another observer.
            if( !observer.isAttached )
                continue;                

            if (Base::getLogLevel() >= Base::LOGLEVEL::D_DEBUG)
            {
                // store name here, maybe it is possible, that observer will be deleted in onChange method, so we do not want to access Iter->first after that
                std::string observerName = (observer.observerPtr)->name() ? (observer.observerPtr)->name() : "<no Name>";

                Base::Timer t;                    
                (observer.observerPtr)->onChange(this, rcReason);  // send OnChange-signal
                if (_allDetachedWhileRunningNotify)
                {
                    _allDetachedWhileRunningNotify = false;
                    break;
                }

                auto myt = t.elapsedMS();

                if (_observerTime.find(observerName) == _observerTime.end())
                    _observerTime[observerName] = myt;
                else
                    _observerTime[observerName] += myt;

                if (myt > 50)
                    cWarn("  Observer (%s) need %f ms", observerName.c_str(), t.elapsedMS());
                else if (myt > 5)
                    cDebug("  Observer (%s) need %f ms", observerName.c_str(), t.elapsedMS());
            }
            else
            {   
                if (observer.observerPtr->__deadVal == 0xBADEAFFE)
                {
                    (observer.observerPtr)->onChange(this, rcReason);  // send OnChange-signal
                    if (_allDetachedWhileRunningNotify)
                    {
                        _allDetachedWhileRunningNotify = false;
                        break;
                    }
                }
                else
                    cWarn("Urgg deleted observer");
            }

        }


        // Is a Observer attached while notify?
        int counter = 10;
        while( !_ObserverSet_AddedLater.empty() )
        {
            _ObserverSet_AddedLaterCopy.clear();
            _ObserverSet_AddedLaterCopy.swap(_ObserverSet_AddedLater);
            for (const auto& observer : _ObserverSet_AddedLaterCopy)
            {
                if (observer.isAttached)
                {
                    if (observer.observerPtr->__deadVal == 0xBADEAFFE)
                    {
                        (observer.observerPtr)->onChange(this, rcReason);  // send OnChange-signal
                        if (_allDetachedWhileRunningNotify)
                            break;
                        _ObserverSet.insert(observer);
                    }
                    else
                        cWarn("Urgg deleted observer");
                }
            }            

            _ObserverSet_AddedLaterCopy.clear();

            if (_allDetachedWhileRunningNotify)
            {
                _allDetachedWhileRunningNotify = false;
                break;
            }

            if( (counter--) <= 0 )
            {
                cWarn("ERROR _ObserverSet_AddedLater, to many repeats!");
                cDebuggerBreak("ERROR notify_internal, to deep recursion!");
                break; 
            }
        }

        // Now process the messages we got while running notify...
        auto copy_messages_WhileRunningNotify = _messages_WhileRunningNotify;
        _messages_WhileRunningNotify.clear();
        for(auto &message : copy_messages_WhileRunningNotify )
        {
            notify_internal( message, deep+1 );
        }
    
    }
    
    void notify(_MessageType& rcReason)
    {
        if (_running_notify)
        {
            _messages_WhileRunningNotify.push_back(rcReason);
            return;
        }
        _running_notify = true;                          
        notify_internal(rcReason, 1);
        _running_notify = false;
        _allDetachedWhileRunningNotify = false;

        auto observerSetCopy = _ObserverSet;
        for (auto observer : observerSetCopy)
        {
            if( !observer.isAttached )
                _ObserverSet.erase( observer );
        }

    }

    /** Get an Observer by name
     * Get a observer by name if the observer reimplements the Name() method.
     * @see Observer
     */
    Observer<_MessageType>* get(const char* Name)
    {
        const char* OName;
        for (auto observer : _ObserverSet)
        {
         
            OName = observer.observerPtr->name();  // get the name
            if (OName && strcmp(OName, Name) == 0)
                return observer.observerPtr;         
        }

        return nullptr;
    }

    // std::vector<Observer<_MessageType>*> getAll()
    //{
    //    std::vector<Observer<_MessageType>*> ret;
    //    for (auto observer : _ObserverSet)
    //    {
    //        ret.push_back(observer.observerPtr);
    //    }
    //    return ret;
    //
    //}

    virtual const char* subject_name(void) { return "NO SUBJECT NAME"; }

    void resetObserverTime() { _observerTime.clear(); }

    std::map<std::string, double> getObserverTime() { return _observerTime; }


    

protected:


    // Compare observers according priority. Higher priority first.
    struct CompareObservers
    {
        bool operator()(const ObserverHolder& o1, const ObserverHolder& o2) const
        {
            if (o1.observerPriority == o2.observerPriority)
                return o1.observerPtr < o2.observerPtr;
            else
                return o1.observerPriority > o2.observerPriority;
        }
    };

        
    typedef std::set<ObserverHolder, CompareObservers> ObserverSetType;

    //std::vector<ObserverHolder> getObserverSortedByPriority( const ObserverSetType& obs )
    //{
    //    std::vector<ObserverHolder> ret( obs.begin(), obs.end() ) ;
    //
    //    std::sort(ret.begin(), ret.end(), [](const ObserverHolder& a,const ObserverHolder& b)
    //        { return a.observerPriority > b.observerPriority; });
    //
    //    return ret;        
    //}

    ObserverSetType _ObserverSet;  /// Set of attached observers
    ObserverSetType _ObserverSet_AddedLater;  /// Set of attached observers at running notify
    ObserverSetType _ObserverSet_AddedLaterCopy;

    bool _running_notify;    
    bool _allDetachedWhileRunningNotify = false;
    std::list<_MessageType> _messages_WhileRunningNotify;
    std::map<std::string, double> _observerTime;
};


}  // namespace Base
