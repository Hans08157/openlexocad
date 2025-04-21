#pragma once

#include <Base/String.h>
#include <OpenLxApp/Document.h>


/** @defgroup OPENLX_EXPORTER Exporter
 */

namespace OpenLxApp
{
/** @brief Base class of all Exporters.
 * @ingroup OPENLX_EXPORTER
 */
class LX_OPENLXAPP_EXPORT Exporter
{
public:
    Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    Exporter() = delete;
    virtual int exportFile(const Base::String& filename) = 0;
    void setSilentMode(bool aFlag);
    bool isInSilentMode() const;
    virtual ~Exporter();

protected:
    bool init();
    std::shared_ptr<OpenLxApp::Document> _doc;
    bool _silentMode = false;
};
}  // namespace OpenLxApp
