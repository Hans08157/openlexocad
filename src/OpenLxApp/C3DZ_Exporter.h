#pragma once

#include <Geom/Pnt.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Exporter.h>

namespace OpenLxApp
{
/** @brief Exports the visible Elements of the Document to an 3DZ file. Elements that are
 * not visible but depend on a visible Element will also be exported
 * (like Openings for a Wall).
 * @ingroup OPENLX_EXPORTER
 */

class LX_OPENLXAPP_EXPORT C3DZ_Exporter : public Exporter
{
public:
    C3DZ_Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    C3DZ_Exporter() = delete;
    virtual ~C3DZ_Exporter() {}
    static std::shared_ptr<C3DZ_Exporter> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    void setExportToClipboard(bool aFlag);
    bool getExportToClipboard() const;

    void setShowDialog(bool aFlag);
    bool getShowDialog(bool aFlag) const;

    void setSelectedOnly(bool aFlag);
    bool getSelectedOnly() const;

    void setActivePoint(const Geom::Pnt& aActivePnt);
    Geom::Pnt getActivePoint() const;

    void setExportVersion(int aVersion);
    int getExportVersion() const;

    void setTextMode(bool aFlag);
    bool getTextMode() const;

    virtual int exportFile(const Base::String& filename) override;

private:
    bool _exportToClipboard = false;
    bool _showDialog = false;
    bool _selectedOnly = false;
    Geom::Pnt _activePnt = Geom::Pnt(0, 0, 0);
    int _exportVersion = 2;
    bool _textMode = false;
};
}  // namespace OpenLxApp