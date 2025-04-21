#pragma once

#include <Base/String.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Element.h>

/** @defgroup OPENLX_IMPORTER Importer
 */


namespace OpenLxApp
{
/** @brief Base class of all Importers.
 * @ingroup OPENLX_IMPORTER
 */
class LX_OPENLXAPP_EXPORT Importer
{
public:
    Importer(std::shared_ptr<OpenLxApp::Document> aDoc);
    Importer() = delete;
    virtual int importFile(const Base::String& filename) = 0;
    void setSilentMode(bool aFlag);
    bool isInSilentMode() const;
    virtual ~Importer();
    virtual std::vector<std::shared_ptr<OpenLxApp::Element>> getImportedElems() const = 0;

    bool init();

protected:
    std::shared_ptr<OpenLxApp::Document> _doc;
    bool _silentMode = false;
};
}  // namespace OpenLxApp
