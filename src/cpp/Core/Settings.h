#pragma once

#include <Base/GlobalId.h>
#include <Base/Log.h>
#include <Base/Translator.h>
#include <Core/ViewerType.h>
#include <Core/CodeProtectionInfo.h>

#include <Geom/Pnt.h>
#include <Geom/Trsf.h>

#include <memory>
#include <vector>
#include <bitset>
#include <string>


class QDialog;
class QTreeWidget;
class QSplitter;

struct CodeExtendedInfoType;
struct CodeProtectionInfo;

namespace Core
{
class SettingsP;
class CoreDocument;
class DocObject;
struct CodeProtectionFlags;
typedef std::shared_ptr<Core::CodeProtectionFlags> pCodeProtectionFlags;

struct LX_CORE_EXPORT UpdateInfo
{
    QString server;
    std::vector<QString> backup_server;
    QString login;
    QString password;
    QString path;
};

struct LX_CORE_EXPORT WindowSettings
{
    int width = 1000;
    int height = 500;
    int x = 0;
    int y = 0;
    bool fullscreen = true;
};


//
// BEWARE !!
//
// This class is PLATFORM-DEPENDENT !
//
// The reason is that the location in the system registry for file extension
// association is VALID ONLY FOR WINDOWS.
//


class LX_CORE_EXPORT Settings
{
public:
    enum CatalogType
    {
        STANDARD,
        OPENBUILT,
        USER,
        USER_USP,
        INTERNAL
    };

    enum CutOptions
    {
        SHOW,
        HIDE,
        ASK
    };

    enum SnapMode
    {
        OLD_MODE = 0,
        NEW_MODE = 1
    };

    enum ShapeTessellationQuality
    {
        coarse = 0,         // .004		* (diagonal of bounding box )
        medium_coarse = 1,  // .002		* (diagonal of bounding box )
        medium_fine = 2,    // .001		* (diagonal of bounding box )
        fine = 3,           // .0005	* (diagonal of bounding box )
        ownImpl = 4
    };

    enum ShapeTessellationMode
    {
        facet_options_visualization = 0,
        facet_options_precise = 1,
        facet_options_expert = 2,
        facet_global = 3
    };

    enum class ShapeCreationMode
    {
        Acis,
        Mesh,
        Inventor,
        MeshOnlyForMultiGeo
    };

    enum class MarkerResolution
    {
        Small,
        Large,
        Medium
    };

    enum class MarkerResolutionPolicy
    {
        Auto,
        Manuall
    };



    void registerSettings();
    void unregisterSettings();

    void saveWindowSettings(int mainWinDimensionX, int mainWinDimensionY, int mainWinPositionX, int mainWinPositionY, bool isMainWinMaximized);
    WindowSettings loadWindowSettings();
    // void saveLexocadLayoutState(const QByteArray &state);
    // bool loadLexocadLayoutState(QByteArray &state);

    ShapeCreationMode getDefaultIFCShapeCreationMode() const;
    void setDefaultIFCShapeCreationMode(ShapeCreationMode m);

    void saveString(const QString& regKey, const QString& text);
    void loadString(const QString& regKey, QString& text);

    void saveDialogGeometry(QWidget* dialog);
    bool loadDialogGeometry(QWidget* dialog);

    void saveTreeWidgetSettings(QTreeWidget* tree);
    bool loadTreeWidgetSettings(QTreeWidget* tree);

    void saveSplitterSettings(QSplitter* splitter);
    bool loadSplitterSettings(QSplitter* splitter);

    void savePieceListDialogSettings(const QString& str, const QByteArray& tableState);
    void loadPieceListDialogSettings(const QString& str, QByteArray& tableState);

    void saveIfcVersionDialogSettings(const QByteArray& data);
    void loadIfcVersionDialogSettings(QByteArray& data);

    void saveIfcImportExceptions(const QByteArray& data);
    void loadIfcImportExceptions(QByteArray& data);

    void saveProxyAuthentication(const QByteArray& data);
    void loadProxyAuthentication(QByteArray& data);

    void saveLoadMaterialDlgSettings(const QByteArray& tableState);
    bool loadLoadMaterialDlgSettings(QByteArray& tableState);

    void saveExtrudedAreaDlgSettings(int profileIndex, const QString& parameter1, const QString& parameter2);
    void loadExtrudedAreaDlgSettings(int& profileIndex, QString& parameter1, QString& parameter2);

    void saveVisibilityDialogSettings(const QByteArray& geometryState, const QByteArray& splitterState);
    bool loadVisibilityDialogSettings(QByteArray& geometryState, QByteArray& splitterState);

    const std::vector<int>& getUserDefFKeys();
    void saveFKey(int fIdx, const QString& alternateActionName);
    void loadFKeys(QStringList& actions);
    QString loadFKey(const uint& functionKeyNumber) const;

    void saveScreenRecorderActive(bool on);
    bool loadScreenRecorderActive();

    void saveScreenRecorderQualityProfile(int qualityProfile);
    int loadScreenRecorderQualityProfile();

    void saveScreenRecorderWindowSize(const QSize& size);
    QSize loadScreenRecorderWindowSize();

    void saveCameraAnimationViewerSize(const QSize& size);
    QSize loadCameraAnimationViewerSize();

    void saveScreenRecorderAskForVideoFileName(bool on);
    int loadScreenRecorderAskForVideoFileName();

    // void saveScreenRecorderQuality(int quality); //Target quantizer
    // int loadScreenRecorderQuality();

    // void saveScreenRecorderFps(int fps);
    // int loadScreenRecorderFps();

    void saveScreenRecorderOversize(bool on);
    bool loadScreenRecorderOversize();
    void saveScreenRecorderOversizeSize(const QSize& size);
    QSize loadScreenRecorderOversizeSize();

    void saveScreenRecorderShowMenu(bool on);
    bool loadScreenRecorderShowMenu();

    void saveScreenRecorderShowKeysAndMouse(bool on);
    bool loadScreenRecorderShowKeysAndMouse();

    void saveScreenRecorderRecordSound(bool recordSound);
    bool loadScreenRecorderRecordSound();

    void saveScreenRecorderShowRedRectangle(bool show);
    bool loadScreenRecorderShowRedRectangle();

    void saveScreenRecorderRecordEvents(bool recordEvents);
    bool loadScreenRecorderRecordEvents();

    void saveScreenRecorderPlayEvents(bool playEvents);
    bool loadScreenRecorderPlayEvents();

    void saveWelcomeScreenVisible(bool on);
    bool loadWelcomeScreenVisible();

    void saveNotificationDialogVisible(const unsigned int id, bool on);
    bool loadNotificationDialogVisible(const unsigned int id) const;

    bool isUserDebugWindowVisible();
    void setUserDebugWindowVisible(bool visible);

    void saveFonts(const QStringList& fonts);
    QStringList loadFonts();

    void saveUserSettings(int cameraAnimationTime, int importMaxPoints);
    void loadUserSettings(int& cameraAnimationTime, int& importMaxPoints);

    void setLastImportedFilePath(QString path);
    QString getLastImportedFilePath();

    void setCurrentScriptFilePath(const QString& path);
    QString getCurrentScriptFilePath() const;

    void setCurrentScriptId(const Base::GlobalId& aScriptId);
    Base::GlobalId getCurrentScriptId() const;

    void setCurrentScriptInsertionPoint(const Geom::Pnt& aInsertionPnt, bool isDragAndDropped, Core::DocObject* aDroppedOnObject);
    Geom::Pnt getCurrentScriptInsertionPoint(bool& isDragAndDropped, Core::DocObject*& aDroppedOnObject) const;

    void setBuildingBlocksDir(std::string dir);
    std::string getBuildingBlocksDir();
    void setMaterialDir(std::string dir);
    std::string getMaterialDir();

    void setIconsDir(std::string dir);
    std::string getIconsDir();

    static void saveLanguage(CTranslator::Language language);
    static CTranslator::Language loadLanguage();

    void enable_polgonoffset(bool on);
    bool is_polgonoffset_enabled();

    CatalogType getCatalogType();
    void setCatalogType(CatalogType);

    // void saveUseSaveReminder(bool on);
    // bool loadUseSaveReminder();

    void setTest(bool on);
    bool test() const;

    bool developer() const;
    bool loadLccDataOnStartup() const;

    void setMacroRecorderActive(bool on);
    bool macroRecorderActive();

    // void setTranslationStepForPropertyView(double value);
    // double getTranslationStepForPropertyView();

    void setRotationStepForPropertyView(double value);
    double getRotationStepForPropertyView();

    void saveRecentFiles(const QStringList& list);
    bool loadRecentFiles(QStringList& list);

    unsigned int getMaxRecentFiles();
    void setMaxRecentFiles(unsigned int value);

    QString getUserCatalogDirInCadworkCat();
    QString getUserCatalogDirInUserProfile();
    QString getUserCatalogDir(bool ignoreStandalone = false);
    void setUserCatalogDir(const QString& dir);

    // Settings related to the software XDEEA
    QString getXdeeaExePath();
    void setXdeeaExePath(const QString& value);

    QString getBackupDir(bool ignoreStandalone = false);
    // void setBackupDir(const QString &dir);

    int getNumberOfBackupFiles();
    int getStandaloneNumberOfBackupFiles();
    void setNumberOfBackupFiles(int count);

    int getIntervalOfBackupFiles();
    int getStandaloneIntervalOfBackupFiles();
    void setIntervalOfBackupFiles(int value);
            
    void loadCodeProtectionFlags(bool forceReload = true);    
    pCodeProtectionFlags getCodeProtectionFlags() const;
    std::vector<int> codeProtectionTest(const std::vector<int>& requiredCodes) const;
    const std::vector<bool>& getDisabledCodes() const;
    void setDisabledCodes(const std::vector<bool>& disabledCodes);

    static Core::Settings* getInstance();
    Core::Settings* init(int argc, char** argv);

    void setSubProductID_Standard();
    void setSubProductID_IfcUser();
    void setSubProductID_Plugin();
    bool isSubProductID_Standard();
    bool isSubProductID_IfcUser();
    bool isSubProductID_Plugin();
    std::string getSubProductIDAsString();
    QString getPluginDir();
    void setPluginDir(const QString& dir);


    // Special Andreas, the version is from the cadwork.dir/exe_XX
    bool getVersionFromCurrentExeDir(int& version);
    QString getCadworkDir() const;
    QString getCadworkPCLIBDir() const;
    QString getCadworkCat() const;    
    QString getCadworkUserprofile(bool ignoreStandalone = false) const;
    QString getCadworkUserprofileWithVersion() const;
    QString getCadworkClipboard() const;
    int getCadworkNumberOfBackupFiles() const;
    void setCadworkNumberOfBackupFiles(int value);
    int getCadworkIntervalOfBackupFiles() const;
    void setCadworkIntervalOfBackupFiles(int value);

    bool isCadwork3dInstalled() const;

    QString getPath2TestDocuments() const;

    QColor getBackgroundColor();
    void setBackgroundColor(const QColor& color);

    QColor getGroundPlateColor();
    void setGroundPlateColor(const QColor& color);

    void setOpenFileDir(QString dir);
    QString getOpenFileDir();

    void setTextureOpenFileDir(QString dir);
    QString getTextureOpenFileDir();

    void setCutOptions(CutOptions options);
    CutOptions getCutOptions();
    
    Core::CodeProtectionInfo getCodeProtectionInfo() const;
    
    const QString& getClientNr();
    QLocale::Country getClientCountry() const;
    QString getCodeProtectionNodeName();

    /// Sets the preference key and value for a specified Lexocad module.
    /// Example: setModulePreference("IfcImport", "preference_ifc_color", "0")
    void setModulePreference(const QString& moduleName, const QString& key, const QString& value);
    /// Returns the value of a preference key for a module.
    /// Example: getModulePreference("IfcImport", "preference_ifc_color")
    QString getModulePreference(const QString& moduleName, const QString& key, const QString& defaultValue = QString());

    void setViewAnimation(bool on);
    bool getViewAnimation() const;

    void setShowScaleHandles(bool on);
    bool getShowScaleHandles() const;

    void setEnableZBufferPDFHack(bool on);
    bool getEnableZBufferPDFHack() const;

    void setTexturesAllFaces(bool on);
    bool getTexturesAllFaces() const;

    void setShowConsole(bool on);
    bool getShowConsole();

    void setWithDebugger(bool on);
    bool getWithDebugger();

    void setStyleSheetName(const QString& name);
    QString getStyleSheetName();
    QString loadStyleSheet(const QStringList& list);

    QString getOpenLxVersionString() const;
    void setOpenLxVersionString(const QString& aVersion);

    bool canUseAcis();

    // void setWoodUser(bool on);

    void setForceWoodUser(bool on);
    bool getForceWoodUser() const;
    bool getWoodUser();

    void setOpenBuiltUser(bool on);
    bool getOpenBuiltUser();

    void setIfcUser(bool on, bool persistent = false);
    bool getIfcUser();

    void setIfcViewerFile(QString a);
    QString getIfcViewerFile();
    bool isImportFromCadWorkBimViewer();

    // void setIfcSettings(bool on, bool persistent = false);
    // bool getIfcSettings();

    void setDebugUser(bool on, bool persistent = false);
    bool getDebugUser(bool persistent = false);

    bool getBaubitUser();
    void setBaubitUser(bool on);

    bool isConceptionUserByDefault();
    bool isConceptionUser();
    void setConceptionUser(bool on);

    void setDownloadPdbFilesAndDebugLinks(bool on);
    bool getDownloadPdbFilesAndDebugLinks();

    void setAcisPartEnabled(bool on);
    bool getAcisPartEnabled();

    void setLODEnabled(bool on);
    bool getLODEnabled() const;

    void saveIntegratedL2DLayoutState(const QByteArray& state);
    bool loadIntegratedL2DLayoutState(QByteArray& state);

    void setShowTextures(bool on);
    bool getShowTextures() const;

    void setShowComponentTypeTextures(bool on);
    bool getShowComponentTypeTextures() const;

    void set_HPK_UseRain(bool yesno);
    bool get_HPK_UseRain() const;

    void setCalculateViewprovider(bool on);
    bool getCalculateViewprovider() const;

    /// Sets an alternative path to look for dlls and other application files. -> Needed for cadwork pclib
    void setAlternativeLookupPath(const Base::String& path);
    /// Sets an alternative path to look for dlls and other application files -> Needed for cadwork pclib
    Base::String getAlternativeLookupPath() const;

    Base::String getLexo2DName();
    void setLogLevel(Base::LOGLEVEL, bool persistent = false);
    Base::LOGLEVEL getLogLevel();

    bool getAcisVersion(int& major, int& minor, int& point);
    void setAcisVersion(int major, int minor, int point);

    void setRenderWireframe(bool on);
    bool getRenderWireframe() const;
    void setRenderFacets(bool on);
    bool getRenderFacets() const;

    SnapMode getSnapMode() const;
    void setSnapMode(SnapMode);

    void setUngroupMode(bool on);
    bool getUngroupMode() const;

    void setMultiGeoUngroupMode(bool on);
    bool getMultiGeoUngroupMode() const;

    void setShaderMultisampling(bool on);
    bool getShaderMultisampling() const;

    void setAllowMultiViewOnStart(bool on);
    bool getAllowMultiViewOnStart() const;

    int getDebugMessageCounter();
    void resetDebugMessageCounter();
    void incrementDebugMessageCounter();

    void setAcisSaveEntityTextMode(bool on, bool persistent = false);
    bool getAcisSaveEntityTextMode() const;

    void setShapeTessellationQuality(Core::Settings::ShapeTessellationQuality quality);
    Core::Settings::ShapeTessellationQuality getShapeTessellationQuality();

    void set3dzExportCutOpenings(bool on, bool persistent = false);
    bool get3dzExportCutOpenings() const;

    void setShowLayerNumber(bool on);
    bool getShowLayerNumber() const;

    // void setShowLayerZValue(bool on);
    // bool getShowLayerZValue() const;

    void setShowComponentTypeNumber(bool on);
    bool getShowComponentTypeNumber() const;

    void setBeamBothEndsSame(bool on);
    bool getBeamBothEndsSame();

    void setCadworkStyle(bool on);
    bool getCadworkStyle() const;

    void setOSGMode(bool on, bool persistent = false);
    bool getOSGMode() const;

    void setCombinedAcisSaveMode(bool on, bool persistent = false);
    bool getCombinedAcisSaveMode() const;

    void setIFCFastMode(bool on, bool persistent = false);
    bool getIFCFastMode() const;

    void setGlobalViewerScopeWireframeDrawStyle(bool on);
    bool getGlobalViewerScopeWireframeDrawStyle() const;

    void setUseThreads(bool on, bool persistent = false);
    bool getUseThreads() const;

    void setIVExportSelectedFilter(QString filter);
    QString getIVExportSelectedFilter() const;

    void setRunningFromLexocad(bool on);
    bool getRunningFromLexocad() const;

    void setFastRenderMode(bool on, bool persistent = false);
    bool getFastRenderMode() const;

    bool getCheckShapesOnRecompute(int& checkLevel) const;
    void setCheckShapesOnRecompute(bool on, int checkLevel);

    bool getCheckSliverFacesOnRecompute() const;
    void setCheckSliverFacesOnRecompute(bool on);

    bool getCheckFacetedBrepOnRecompute() const;
    void setCheckFacetedBrepOnRecompute(bool on);

    bool getPointCloudMode() const;
    void setPointCloudMode(bool on);

    bool getPointCloudPointPicking() const;
    bool setPointCloudPointPicking(bool on);

    bool getPointCloudPointSelection() const;
    void setPointCloudPointSelection(bool on);

    bool getPointCloudDynamicPointSize() const;
    void setPointCloudDynamicPointSize(bool on, bool persistent = false);

    bool getPointCloudChunkSelectionEnabled() const;
    void setPointCloudChunkSelectionEnabled(bool on);

    bool getPointCoarseLOD() const;
    void setPointCoarseLOD(bool on);

    void setCreateMiniDumpOnCrash(bool on);
    bool getCreateMiniDumpOnCrash();

    void setSoSeparatorCachingEnabled(bool on);
    bool getSoSeparatorCachingEnabled() const;

    void setSoSeparatorCachingEnabledSpecial(bool on);
    bool getSoSeparatorCachingEnabledSpecial() const;

    bool getPointCloudLODenabled() const;
    void setPointCloudLODenabled(bool on);

    bool getShowPointCloudInSecondViewer() const;
    void setShowPointCloudInSecondViewer(bool on);

    bool getSketcherMode() const;
    void setSketcherMode(bool aOn);


    void setViewerGeo(Core::ViewerType viewerType, const QSize& size, const QPoint& pos, bool maximized);
    void getViewerGeo(Core::ViewerType viewerType, QSize& size, QPoint& pos, bool& maximized);

    void setLexocadCode(bool on);
    bool getLexocadCode() const;

    bool getStandalone() const;
    void setStandalone(bool on);
    QString getStandaloneAppDataPath() const;

    bool getShowMeshOrientation() const;
    void setShowMeshOrientation(bool on);

    void setDefaultDoorPreset(QString preset);
    QString getDefaultDoorPreset() const;

    void setDefaultWindowPreset(QString preset);
    QString getDefaultWindowPreset() const;

    void setDefaultFrenchWindowPreset(QString preset);
    QString getDefaultFrenchWindowPreset() const;

    void setDefaultGarageDoorPreset(QString preset);
    QString getDefaultGarageDoorPreset() const;

    bool getNewZooming() const;
    void setNewZooming(bool on);

    bool getCoinShaderMode() const;
    void setCoinShaderMode(bool on, bool persistent = true);

    bool getProfiling() const;
    void setProfiling(bool on);

    bool getMeshCaching() const;
    void setMeshCaching(bool on);

    bool getAcisMeshMultiThreating() const;
    void setAcisMeshMultiThreating(bool on);

    int getFastRenderBatchMaxVertexCount() const;
    void setFastRenderBatchMaxVertexCount(int);

    bool getFastRenderEnableEdges() const;
    void setFastRenderEnableEdges(bool);

    bool getSaveRestoreIfcModelWithDocument() const;
    void setSaveRestoreIfcModelWithDocument(bool on);

    bool getMaterialViewSmallIcons() const;
    void setMaterialViewSmallIcons(bool on);

    bool getOpenMaterialDlgSmallIcons() const;
    void setOpenMaterialDlgSmallIcons(bool on);

    uint64_t getLODMinimalPointCount() const;
    void setLODMinimalPointCount(uint64_t t);

    void setAcisMeshShapeEnabled(bool);
    bool getAcisMeshShapeEnabled() const;

    void setShowPreviewSurfaceForVerticalView(bool on);
    bool getShowPreviewSurfaceForVerticalView();

    void setDeepDebug(bool on);
    bool getDeepDebug() const;

    void setAllowMemoryIsLowMsg(bool on);
    bool getAllowMemoryIsLowMsg() const;

    QString getCadwork3DDir() const;

    void setWallSolveWarning(int status);  // 0=do not show, 1=show once, 2=show always
    int getWallSolveWarning() const;

    const std::string& riSelectedDevice() const;
    void riSetSelectedDevice(const std::string& s);
    bool isVulkanRenderingEnabled() const;
    bool isHoopsRenderingEnabled() const;
    const std::string& riTestScene() const;

    bool disabledLog() const;

    // void setAutoClippingBoxMode(bool on);
    // bool getAutoClippingBoxMode() const;

    void setNewViewProviderUpdate(bool on);
    bool getNewViewProviderUpdate() const;

    void setVisibilityIconHas3States(bool on);
    bool getVisibilityIconHas3States() const;

    void setSaveDialogGeometryInRegistry(bool on);
    bool getSaveDialogGeometryInRegistry() const;

    uint64_t getMetalShapeSelectionFlags() const;
    void setMetalShapeSelectionFlags(uint64_t flags);

    bool isWoodConstructionUser();

    bool isInternalCadworkUser();

    std::pair<int, int> getMinimalModernOpenGLVersion() const;

    void setObjExportUnprotected(bool unprotected);
    bool isObjExportUnprotected() const;

    bool getRealLineThicknessMode() const;
    void setRealLineThicknessMode(bool on);
    const Geom::Trsf& getRealLineThicknessModeTrsf() const;
    void setRealLineThicknessModeTrsf(const Geom::Trsf& trsf);

    Base::String getLxElementTypeIdentifier() const;

    Base::String getDisplayName();

    bool checkResultFromPolyToAcisConverter() const;
    void setCheckResultFromPolyToAcisConverter(bool v);


    bool allowQuadroCard() const;
    Core::UpdateInfo getUpdateInfo();
    bool getUpdateInfos(QString& application, QString& updateDir) const;
    bool getUpdateSetting(QString& organization, QString& application) const;

    void setDrawLocalCoordinateSystem(bool on);
    bool getDrawLocalCoordinateSystem() const;


    void setMarkerResolution(MarkerResolution);
    MarkerResolution getMarkerResolution();

    void setMarkerResolutionPolicy(MarkerResolutionPolicy);
    MarkerResolutionPolicy getMarkerResolutionPolicy();

    double getPickRadius();
    double getPickRadiusVerticesOnly();
    void setPickRadiusVerticesOnly(bool);
    bool isPickRadiusVerticesOnly() const;


    void set4KMointorOrGreater(bool v);
    void setHighDPIMonitor(bool v);
    void setScreenSize(QSizeF s);

    unsigned long getLODLevel_MidRes() const;
    unsigned long getLODLevel_LowRes() const;
    unsigned long getLODLevel_VoidRes() const;


    bool isGridPicking() const;
    void setGridPickung(bool on);

    bool isMidPointPicking() const;
    void setMidPointPickung(bool on);

	bool isIntersectionPointPicking() const;
    void setIntersectionPointPicking(bool on);
    bool isUnitTestingEnabled() const;
    void enableUnitTesting(bool on);

    bool isDefectLinksCheckBoxEnabled() const;
    void enableDefectLinksCheckBox(bool on);

    bool isDefectLinksMessageEnabled() const;
    void enableDefectLinksMessage(bool on);

    bool getAllowAutoSequencer() const;
    void setAllowAutoSequencer(bool on);

    bool getAllowPelicanMultithreading() const;
    void setAllowPelicanMultithreading(bool on);

    QString getCustomBimTeamOrigin() const;
    void setCustomBimTeamOrigin(const QString& value);

    static bool isPublicVersion();
    static std::string getActiveChannel();
    bool hasPreviousVersionToSave();
    static std::pair<int, int> getPreviousVersionToSave();
    static bool showNewVersionMessage(std::pair<int, int> appVersionOfOpeningDocument);
    bool isInternalUser();
    static bool isUpdateCI_Start();
    static bool isUpdateConceptionUser();
    static bool isUpdateLexocadUser();


    /// Is this Lexocad running inside of cadwork.dir?
    bool lexocadIsIncadworkDir(QString& errorMessage);
    /// Get path to ci_start.exe
    bool get_CI_Start_FilePath(QString& ci_start_filepath, QString& errorMessage);

    bool getShowAlwaysBoundingBoxOnSelectionAction() const;
    void setShowAlwaysBoundingBoxOnSelectionAction(bool);

    void setSeveralOneVisibilityMode(bool on);
    bool getSeveralOneVisibilityMode() const;

    bool isCadworkBimViewerEnabled() const;
    void setCadworkBimViewerEnabled(bool) const;

    double getSizeForHugeBoundingBox() const;

    size_t selectionTimeOutInSeconds() const;
    void   setSelectionTimeOutInSeconds(size_t);

    void setDebugViewer(std::bitset<8> aViewerDebugBits);
    bool isDebugViewer(int aViewerId) const;
    bool isDebugAnyViewer() const;

private:
    Settings() = default;
    Settings(int argc, char** argv);
    ~Settings(){};

    Core::SettingsP* _pimpl = nullptr;
    static Core::Settings* _instance;

    QString _getNotificationDialogKey(const unsigned int id) const;
};


}  // namespace Core
