#pragma once

#include <OpenLxApp/Document.h>
#include <OpenLxApp/Exporter.h>


namespace OpenLxApp
{
/** @brief Exports the visible Elements of the Document to an WebGl (html) file.
 * @ingroup OPENLX_EXPORTER
 */
class LX_OPENLXAPP_EXPORT WebGL_Exporter : public Exporter
{
public:
    WebGL_Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    WebGL_Exporter() = delete;
    virtual ~WebGL_Exporter() {}
    static std::shared_ptr<WebGL_Exporter> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    void setSingleHtmlFile(bool aFlag);
    bool getSingleHtmlFile() const;
    virtual int exportFile(const Base::String& aFileOrDirName) override;

private:
    bool _singleHtmlFile = false;
};
}  // namespace OpenLxApp