#pragma once

#include <OpenLxApp/Document.h>
#include <OpenLxApp/Importer.h>

namespace Gui
{
class CmdImportFile;
}

namespace OpenLxApp
{
/** @brief Imports an Open Inventor (*iv) file.
 * @ingroup OPENLX_IMPORTER
 */
class LX_OPENLXAPP_EXPORT IV_Importer : public Importer
{
public:
    IV_Importer(std::shared_ptr<OpenLxApp::Document> aDoc);
    IV_Importer() = delete;
    virtual ~IV_Importer() {}
    static std::shared_ptr<IV_Importer> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    virtual int importFile(const Base::String& filename) override;
    virtual std::vector<std::shared_ptr<OpenLxApp::Element>> getImportedElems() const override;

    bool getCreateLayer() const;
    void setCreateLayer(bool aValue);

    bool getAsExtenalFile() const;
    void setAsExternalFile(bool aValue);

private:
    Gui::CmdImportFile* _cmd = nullptr;

    bool _createLayer = true;
    bool _asExternalFile = false;
};
}  // namespace OpenLxApp