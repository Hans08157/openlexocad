#pragma once

#include <OpenLxApp/Document.h>
#include <OpenLxApp/Exporter.h>


namespace OpenLxApp
{
/** @brief Exports the visible Elements of the Document to a SAT file.
 * @ingroup OPENLX_EXPORTER
 */
class LX_OPENLXAPP_EXPORT SAT_Exporter : public Exporter
{
public:
    SAT_Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    SAT_Exporter() = delete;
    virtual ~SAT_Exporter() {}
    static std::shared_ptr<SAT_Exporter> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    virtual int exportFile(const Base::String& filename) override;

    void setAcisVersion(int aVersion);
    int getAcisVersion() const;

private:
    int _acisVersion = -1;
};
}  // namespace OpenLxApp