#pragma once

#include <Base/GlobalId.h>
#include <Base/String.h>
#include <Geom/Pnt.h>

#include <memory>

namespace OpenLxApp
{
class Element;

/**
 * @brief The 'ActiveScript' is the script that is
 * currently been executed ( the script's '__main__'
 * function is called ).
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT ActiveScript
{
public:
    ActiveScript(void);
    ~ActiveScript(void);

    Base::String getFilePath() const;
    Base::GlobalId getScriptId() const;
    bool isDragAndDropped() const;
    Geom::Pnt getInsertionPoint() const;
    std::shared_ptr<Element> getDroppedOnElement() const;

private:
    Base::String _filePath = L"";
    Base::GlobalId _scriptId = Base::GlobalId();
    bool _isDragAndDropped = false;
    Geom::Pnt _insertionPoint = Geom::Pnt(0, 0, 0);
    std::shared_ptr<Element> _droppedOnElement;
};

}  // namespace OpenLxApp