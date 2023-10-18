#include <Shlobj.h>
#include <QSettings>

namespace registerSettings
{

/*!
* Write the application settings in the system registry.
* For now, works only on Windows platform.
*/
void registerSettings()
{
    // Format the commands

    QString exeDir = QDir::toNativeSeparators(qApp->applicationDirPath() + "\\");

    QFileInfo fi = QFileInfo(qApp->applicationFilePath());
    QString exeName = fi.completeBaseName();
    exeName.append(".exe");

    QString openCommand("\"");
    openCommand.append(exeDir);
    openCommand.append(exeName);
    openCommand.append("\" \"%1\" \"%2\"");         // Default open command

    QString newCommand("\"");
    newCommand.append(exeDir);
    newCommand.append(exeName);
    newCommand.append("\" \"%2\"");         // Default new command

    // Format the defaultIcon key value
    QString defaultIcon = exeDir;
    defaultIcon.append(exeName);
    defaultIcon.append(",0");

    QString obzIcon = exeDir;
    obzIcon.append(exeName);
    obzIcon.append(",1");

    QString ifcIcon = exeDir;
    ifcIcon.append(exeName);
    ifcIcon.append(",2");

    QString lxzFile = exeDir;
    lxzFile.append("files_for_userprofil\\Lexocad\\init\\init.lxz");

	QSettings settings("HKEY_CLASSES_ROOT",QSettings::NativeFormat);

	if( !settings.isWritable() )
	{
		qDebug("Cannot write QSettings, not writeable!");
		return;
	}

    /*
	* .lxz
	*/
	QString previousValue = settings.value(".lxz/.").toString();
    if (previousValue.isEmpty() || previousValue.toLower() != "cadwork.lxz")
    {
		// Write the .lxz key in the HKEY_CLASSES_ROOT
		settings.setValue(".lxz/.","Lexocad.lxz");
        settings.setValue(".lxz/ShellNew/FileName", lxzFile);
        settings.setValue("Lexocad.lxz/.", "Lexocad lxz");
		settings.setValue("Lexocad.lxz/DefaultIcon/.", defaultIcon);
		settings.setValue("Lexocad.lxz/Shell/Open/.", "Lexocad");
		settings.setValue("Lexocad.lxz/Shell/Open/command/.", openCommand);
        settings.setValue("Lexocad.lxz/Shell/New/.", "");
		settings.setValue("Lexocad.lxz/Shell/New/command/.", newCommand);
        
		if( settings.status() != QSettings::NoError)
            qDebug("ERROR: in Write Settings");
    }

	/*
	* .caz
	*/
    previousValue = settings.value(".caz/.").toString();
    if (previousValue.isEmpty() || previousValue.toLower() != "cadwork.caz")
    {
		// Write the .caz key in the HKEY_CLASSES_ROOT
		settings.setValue(".caz/.","Lexocad.caz");
		settings.setValue("Lexocad.caz/DefaultIcon/.", defaultIcon);
		settings.setValue("Lexocad.caz/Shell/Open/.", "Lexocad");
		settings.setValue("Lexocad.caz/Shell/Open/command/.", openCommand);
        settings.setValue("Lexocad.caz/Shell/New/.", "");
		settings.setValue("Lexocad.caz/Shell/New/command/.", newCommand);
        
		if( settings.status() != QSettings::NoError)
            qDebug("ERROR: in Write Settings");
    }

	/*
	* -ab-.obcaz
	*/
	// Always overwrite any previous keys
	// Write the .obz key in the HKEY_CLASSES_ROOT
	settings.setValue(".obcaz/.","Lexocad.obcaz");
	settings.setValue("Lexocad.obcaz/DefaultIcon/.", obzIcon);
	settings.setValue("Lexocad.obcaz/Shell/Open/.", "Lexocad");
	settings.setValue("Lexocad.obcaz/Shell/Open/command/.", openCommand);
    settings.setValue("Lexocad.obcaz/Shell/New/.", "");
	settings.setValue("Lexocad.obcaz/Shell/New/command/.", newCommand);

	if( settings.status() != QSettings::NoError)
		qDebug("ERROR: in Write Settings");

	/*
	* .cas
	*/
	// Write the .cas key in the HKEY_CLASSES_ROOT
	settings.setValue(".cas/.","Lexocad.cas");
	// No Icon - Andreas' wish - -mh- 2007-10-21
	//settings.setValue("Lexocad.cas/DefaultIcon/.", defaultIcon);
	settings.setValue("Lexocad.cas/DefaultIcon/.", "");
	settings.setValue("Lexocad.cas/Shell/Open/.", "Lexocad");
	settings.setValue("Lexocad.cas/Shell/Open/command/.", "\""+exeDir+"SendMail.exe\" \"%1\"");// Send mail with system info and files .cas and .caz

	if( settings.status() != QSettings::NoError)
		qDebug("ERROR: in Write Settings");

    /*
    * .ifc
    */
    // Always overwrite any previous keys
    // Write the .ifc key in the HKEY_CLASSES_ROOT
    settings.setValue(".ifc/.","Lexocad.ifc");
    settings.setValue("Lexocad.ifc/DefaultIcon/.", ifcIcon);
    settings.setValue("Lexocad.ifc/Shell/Open/.", "Lexocad");
    settings.setValue("Lexocad.ifc/Shell/Open/command/.", openCommand);

    if( settings.status() != QSettings::NoError)
	    qDebug("ERROR: in Write Settings");

	/*
	* .obz
	*/
	// Always overwrite any previous keys
	// Write the .obz key in the HKEY_CLASSES_ROOT
	settings.setValue(".obz/.","Lexocad.obz");
	settings.setValue("Lexocad.obz/DefaultIcon/.", obzIcon);
	settings.setValue("Lexocad.obz/Shell/Open/.", "Lexocad"); //settings.setValue("Lexocad.obz/Shell/Open/.", "OpenBuiltCAD");
	settings.setValue("Lexocad.obz/Shell/Open/command/.", openCommand);
    settings.setValue("Lexocad.obz/Shell/New/.", "");
	settings.setValue("Lexocad.obz/Shell/New/command/.", newCommand);

	if( settings.status() != QSettings::NoError)
		qDebug("ERROR: in Write Settings");

    #if defined(_WIN32) || defined(_WIN64)
        SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, NULL, NULL);
        //SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, NULL, NULL);
    #endif
}

} // namespace
