#pragma once

#include <OpenLxApp/Document.h>
#include <OpenLxApp/Exporter.h>


namespace OpenLxApp
{
/** @brief Exports the visible Elements of the Document to an OBJ file.
 * The point coordinates can be written out in the following order:
 * YXMODE   -> Y|X|Z
 * ESRIMODE -> X|Z|Y
 * DEFAULT  -> X|Y|Z
 * @ingroup OPENLX_EXPORTER
 */
class LX_OPENLXAPP_EXPORT OBJ_Exporter : public Exporter
{
public:
    OBJ_Exporter(std::shared_ptr<OpenLxApp::Document> aDoc);
    OBJ_Exporter() = delete;
    virtual ~OBJ_Exporter() {}
    static std::shared_ptr<OBJ_Exporter> createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    enum class CoordinateOrder
    {
        DEFAULT = 0,  // -> X|Y|Z
        YXMODE = 1,   // -> Y|X|Z
        ESRIMODE = 2  // -> X|Z|Y
    };

    void setHeader(const Base::String& aHeader);
    void setWithMaterials(bool aFlag);
    void setMerge(bool aFlag);
    void setCoordinateOrder(CoordinateOrder aCoordOrder);

    Base::String getHeader() const;
    bool getWithMaterials() const;
    bool getMerge() const;
    CoordinateOrder getCoordinateOrder() const;


    virtual int exportFile(const Base::String& filename) override;


private:
    Base::String _header;
    bool _withMaterials = true;
    bool _merge = false;
    bool _yxMode = false;
    bool _esriMode = false;
};
}  // namespace OpenLxApp