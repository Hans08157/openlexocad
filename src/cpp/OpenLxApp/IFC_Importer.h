#pragma once

#include <LxIfcBase/LxIfcModel.h>
#include <LxIfcDataBridge/IfcDataBridge.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Importer.h>

namespace Gui
{
class CmdImportFile;
}

namespace OpenLxApp
{
/** @brief Imports an IFC file.
 * @ingroup OPENLX_IMPORTER
 */
class LX_OPENLXAPP_EXPORT IFC_Importer : public Importer
{
public:
    IFC_Importer(std::shared_ptr<OpenLxApp::Document> aDoc);
    IFC_Importer() = delete;
    virtual ~IFC_Importer() {}
    static std::shared_ptr<IFC_Importer> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    virtual int importFile(const Base::String& filename) override;
    virtual std::vector<std::shared_ptr<OpenLxApp::Element>> getImportedElems() const override;

    std::shared_ptr<LxIfcDataBridge::IfcDataBridge> getDataBridge() const;
    std::shared_ptr<LxIfcBase::LxIfcModel> getModel() const;

private:
    Gui::CmdImportFile* _cmd = nullptr;
};
}  // namespace OpenLxApp