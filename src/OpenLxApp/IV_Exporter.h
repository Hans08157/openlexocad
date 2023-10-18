#pragma once

#include <OpenLxApp/Document.h>
#include <OpenLxApp/Exporter.h>


namespace OpenLxApp
{
/** @brief Exports the visible Elements of the Document to an IV file.
 * @ingroup OPENLX_EXPORTER
 */
class LX_OPENLXAPP_EXPORT IV_Exporter : public Exporter
{
public:
    IV_Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    IV_Exporter() = delete;
    virtual ~IV_Exporter() {}
    static std::shared_ptr<IV_Exporter> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    virtual int exportFile(const Base::String& filename) override;

private:
};
}  // namespace OpenLxApp