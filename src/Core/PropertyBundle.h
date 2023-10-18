#pragma once

#include <Core/PropertyContainer.h>

typedef std::map<std::string, Core::Property*> PropertyMap;
typedef std::map<std::string, Core::PropertyValue> PropertyValueMap;


namespace Core
{
template <typename T = Core::PropertyContainer>
class PropertyBundle : public Core::PropertyContainer
{
public:
    /// Creates a PropertyBundle from a PropertyContainer type and copies all properties from the PropertyContainer to the PropertyBundle
    PropertyBundle()
    {
        // Do we have this type already?
        Core::PropertyValueMap pvm;
        if (Core::Property::getRegisteredProperties(T::getClassTypeId(), pvm))
        {
            // Add properties from registry
            Core::PropertyValueMap::const_iterator it;
            for (it = pvm.begin(); it != pvm.end(); ++it)
            {
                Core::PropertyValue pv = it->second;
                Core::PropertyContainer::addProperty(pv.propertyType, pv.propertyName, pv.value);
            }
        }
        else
        {
            // Make new
            T* t = new T;
            if (t)
            {
                // const Core::PropertyMap& pm = t->getPropertyMap();
                Core::PropertyMap pm;
                t->getPropertyMap(pm);
                Core::PropertyMap::const_iterator it;
                for (it = pm.begin(); it != pm.end(); ++it)
                {
                    Core::Property* p = it->second;
                    std::string pName = it->first;
                    Core::PropertyValue pv(pName, p->getTypeId(), p->getVariant());
                    pvm[pName] = pv;
                    Core::PropertyContainer::addProperty(p->getTypeId(), pName, p->getVariant());
                }

                // Add to registry
                Core::Property::registerProperties(T::getClassTypeId(), pvm);
                delete t;
            }
        }
    }
    /// Copy constructor
    PropertyBundle(const PropertyBundle<T>& other) { Core::PropertyContainer::addPropertiesFrom(&other); }

    /// Adds a property to the bundle. Returns 'true' on success, 'false' on failure
    template <typename PropType>
    bool addProperty(const std::string& name, const Core::Variant& defaultValue)
    {
        return Core::PropertyContainer::addProperty(PropType::getClassTypeId(), name, defaultValue);
    }

    PropertyBundle<T>& operator=(const PropertyBundle<T>& other)
    {
        if (*this == other)
            return *this;
        Core::PropertyContainer::removeAllProperties();
        Core::PropertyContainer::addPropertiesFrom(&other);
        return *this;
    }

    bool operator==(const PropertyBundle<T>& other) const { return Core::PropertyContainer::hasSameValuesAs(&other); }

    bool operator!=(const PropertyBundle<T>& other) const { return !(*this == other); }
};

}  // namespace Core
