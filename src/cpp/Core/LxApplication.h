#pragma once 

#include <QApplication>
#include <QMessageBox>
#include <QDebug>



class LxApplication : public QApplication
{
public:
    LxApplication(int& argc, char** argv) : QApplication(argc, argv) 
    {}

    virtual bool winEventFilter(MSG* /*msg*/, long* /*result*/)
    {        
        return false;
    }

    virtual bool notify( QObject * receiver, QEvent *  event ) override
    {
     
        if( catchExceptions )
        {
            try 
            {
                return QApplication::notify(receiver, event);
            }
            catch( std::runtime_error& er )
            {
                QString msg = QString("Uncaught Exception! ") + QString(er.what());
                QMessageBox::critical(0, "Exception", msg );                            
            }
            catch(const std::exception& ex)
            {
                QString msg = QString("Uncaught Exception! ") + QString(ex.what());
                QMessageBox::critical(0, "Exception", msg );                                            
            }
            catch(...)
            {
                // may be handle exception here ...
                // TODO Dietmar
                qDebug() << "Attention. Uncaught Exception! Forgot to catch exception?";

                // HPK 2021-09-23: Deactivated critical message. It drives Andreas crazy.
                // TODO -> Dietmar
                // QMessageBox::critical(0, "Attention", QString("<b>Uncaught Exception! Forgot to catch exception?</b>"));            
            }               
        }
        else
            return QApplication::notify(receiver, event);
        

        return false;
     
    }

    

    
    bool catchExceptions = true;

    

};

#define lxApp (static_cast<LxApplication *>(QCoreApplication::instance()))
