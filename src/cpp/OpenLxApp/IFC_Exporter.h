#pragma once

#include <LxIfcBase/LxIfcModel.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Exporter.h>


namespace OpenLxApp
{
/** @brief Exports the visible Elements of the Document to an IFC file. Elements that are
 * not visible but depend on a visible Element will also be exported
 * (like Openings for a Wall).
 * @ingroup OPENLX_EXPORTER
 */
class LX_OPENLXAPP_EXPORT IFC_Exporter : public Exporter
{
public:
    IFC_Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    IFC_Exporter() = delete;
    virtual ~IFC_Exporter() {}
    static std::shared_ptr<IFC_Exporter> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    bool buildModel();
    std::shared_ptr<LxIfcBase::LxIfcModel> getModel() const;

    void setCheckComplexity(bool aFlag);
    bool getCheckComplexity() const;
    void setIfcVersion(int aVersion);
    int getIfcVersion() const;
    void setExportUndefinedElements(int aValue);
    int getExportUndefinedElements() const;

    virtual int exportFile(const Base::String& filename) override;

private:
    bool mCheckComplexity = false;
    int mIfcVersion = 3;
    int mExportUndefinedElements = -1;
    std::shared_ptr<LxIfcBase::LxIfcModel> mModel;
    Core::Command* mCmd = nullptr;
};
}  // namespace OpenLxApp