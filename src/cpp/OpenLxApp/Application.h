#pragma once



/** @defgroup OPENLX_FRAMEWORK Framework
 */

#include <Base/String.h>
#include <OpenLxApp/ActiveScript.h>

#include <memory>

class QApplication;

namespace App
{
class Application;
}

namespace OpenLxApp
{
class Document;
class ApplicationP;

struct LX_OPENLXAPP_EXPORT LoadPlugins
{
    LoadPlugins()
    {
        ElementExtension = true;
        ElementExtensionGui = true;
        VPFreeExport = false;
        CdwkVariant = false;
        CdwkVariantGui = false;
    }

    bool ElementExtension;
    bool ElementExtensionGui;
    bool VPFreeExport;
    bool CdwkVariant;
    bool CdwkVariantGui;
};

/**
 * @brief The one and only Application
 *
 * @ingroup  OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT Application
{
public:
    Application();
    ~Application(void);

    static Application* getInstance(void);
    static void release();
    /// Creates a new document
    std::shared_ptr<Document> newDocument(const Base::String& name = L"");
    /// Creates a new VariantTransferDocument
    std::shared_ptr<Document> newVariantTransferDocument(const Base::String& name = L"");
    /// Closes the document
    void closeDocument(std::shared_ptr<Document> doc, bool forceClose = false);
    /// Closes all documents
    void closeAllDocuments();
    /// Returns the active document. Creates a new one it createIfNeeded = true.
    std::shared_ptr<Document> getActiveDocument(bool createIfNeeded = false);
    /// Returns the active script.
    ActiveScript getActiveScript() const;
    /// Closes the application
    void closeApplication();
    /// Sets an alternative path to look for dlls and other application files
    void setAlternativeLookupPath(const Base::String& path);
    /// Creates a QApplication
    static void initQt(int argc, char* argv[]);
    /// Creates a QApplication
    static void initQt();
    /// Sets which plugins should be loaded at startup
    static void setPluginsToLoad(const LoadPlugins& lp);
    ///
    static LoadPlugins s_lp;

private:
    static Application* _instance;
    ApplicationP* _pimpl;
    static QApplication* s_qapp;
};
}  // namespace OpenLxApp