#pragma once 

#include <QDomElement>
#include <vector>

namespace Core
{
class Property;
class PropertyContainer;

class LX_CORE_EXPORT PropertySetManager
{
public:
    static bool addToContainer(const std::vector<PropertyContainer*>& containers, const QString& xmlname);

private:
    static PropertySetManager& instance();
    std::vector<PropertyContainer*> _containers;

    void _clear();
    bool _addPropertyToContainer(Core::Property* prop, const std::string& pName, PropertyContainer* pc);

    bool _load(const QString fname);

    bool _processAllowedContainers(const QDomElement elem);

    void _processProperty(const QDomElement elem, QString& name, QString& type);

    void _processPropertyText(const QDomElement elem, const QString name);
    void _processPropertyEnum(const QDomElement elem, const QString name);
};

}  // namespace Core
