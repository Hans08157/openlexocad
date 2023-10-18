#pragma once

#pragma warning(disable : 5054)
#include <QEvent>
#include <QLineEdit>


static const QEvent::Type MessageEventType = QEvent::Type(QEvent::User + 310);

namespace Base
{
class LX_BASE_EXPORT MessageEvent

#ifndef SWIG
    : public QEvent
#endif

{
public:
    MessageEvent(QString message, void* data) : QEvent(MessageEventType)
    {
        _message = message;
        _data = data;
    }
    QString _message;
    void* _data;
};

class MessageBase;

class LX_BASE_EXPORT MessageInterface
{
public:
    enum standard_button
    {
        yes = 1,
        no = 2,
        cancel = 3
    };

    virtual void showMessage(const QString& message) = 0;
    virtual void postMessage(const QString& message) = 0;

    virtual void showMessageBoxInformation(const QString& title, const QString& text, QWidget* parent = nullptr, bool silent = false) = 0;
    virtual void showMessageBoxWarning(const QString& title, const QString& text, QWidget* parent = nullptr, bool silent = false) = 0;
    virtual void showMessageBoxError(const QString& title, const QString& text, QWidget* parent = nullptr, bool silent = false) = 0;
    virtual bool showMessageBoxQuestionYesNo(const QString& title,
                                             const QString& text,
                                             standard_button defaultChoice = yes,
                                             QWidget* parent = nullptr,
                                             bool* checkboxShowAgain = nullptr,
                                             int manualLinkMessageId = -1) = 0;
    virtual standard_button showMessageBoxQuestionYesNoCancel(const QString& title,
                                                              const QString& text,
                                                              standard_button defaultChoice = yes,
                                                              QWidget* parent = nullptr) = 0;
    virtual int showMessageBoxQuestion(const QString& title,
                                       const QString& text,
                                       const QString& text_1,
                                       const QString& text_2,
                                       const QString& text_3,
                                       QWidget* parent = nullptr) = 0;

    virtual void setMessageReciever(MessageInterface* member) = 0;
    virtual MessageInterface* getMessageReciever() = 0;
    virtual void setPostMessageReciever(QObject* postMessagereceiver) = 0;
    virtual void debugMessage(const QString& id, const QString& text) = 0;

    virtual double getDoubleDialog(const QString& title,
                                   const QString& label,
                                   double value = 0,
                                   double min = -2147483647,
                                   double max = 2147483647,
                                   int decimals = 1,
                                   bool* ok = nullptr) = 0;
    virtual int getIntDialog(const QString& title,
                             const QString& label,
                             int value = 0,
                             int min = -2147483647,
                             int max = 2147483647,
                             int step = 1,
                             bool* ok = nullptr) = 0;
    virtual QString getTextDialog(const QString& title,
                                  const QString& label,
                                  QLineEdit::EchoMode mode = QLineEdit::Normal,
                                  const QString& text = QString(),
                                  bool* ok = 0) = 0;
    virtual QString getItem(const QString& title,
                            const QString& label,
                            const QStringList& items,
                            int current = 0,
                            bool editable = true,
                            bool* ok = nullptr) = 0;

protected:
    MessageInterface* _member = nullptr;
    QObject* _postMessagereceiver = nullptr;
};

class LX_BASE_EXPORT MessageBase : public MessageInterface
{
public:
    static MessageBase& instance();

    virtual void showMessage(const QString& message);

    virtual void showMessageBoxInformation(const QString& title, const QString& text, QWidget* parent = nullptr, bool silent = false);
    virtual void showMessageBoxWarning(const QString& title, const QString& text, QWidget* parent = nullptr, bool silent = false);
    virtual void showMessageBoxError(const QString& title, const QString& text, QWidget* parent = nullptr, bool silent = false);
    virtual bool showMessageBoxQuestionYesNo(const QString& title,
                                             const QString& text,
                                             standard_button defaultChoice = yes,
                                             QWidget* parent = NULL,
                                             bool* checkboxShowAgain = nullptr,
                                             int manualLinkMessageId = -1);
    virtual standard_button showMessageBoxQuestionYesNoCancel(const QString& title,
                                                              const QString& text,
                                                              standard_button defaultChoice = yes,
                                                              QWidget* parent = nullptr);
    virtual int showMessageBoxQuestion(const QString& title,
                                       const QString& text,
                                       const QString& text_1,
                                       const QString& text_2,
                                       const QString& text_3,
                                       QWidget* parent = nullptr);

    virtual void debugMessage(const QString& id, const QString& text);
    virtual void setMessageReciever(MessageInterface* member);
    virtual MessageInterface* getMessageReciever();
    virtual void setPostMessageReciever(QObject* postMessagereceiver);
    virtual void postMessage(const QString& message);

    virtual double getDoubleDialog(const QString& title,
                                   const QString& label,
                                   double value = 0,
                                   double min = -2147483647,
                                   double max = 2147483647,
                                   int decimals = 1,
                                   bool* ok = nullptr);
    virtual int
    getIntDialog(const QString& title, const QString& label, int value = 0, int min = -2147483647, int max = 2147483647, int step = 1, bool* ok = 0);
    virtual QString getTextDialog(const QString& title,
                                  const QString& label,
                                  QLineEdit::EchoMode mode = QLineEdit::Normal,
                                  const QString& text = QString(),
                                  bool* ok = nullptr);
    virtual QString getItem(const QString& title,
                            const QString& label,
                            const QStringList& items,
                            int current = 0,
                            bool editable = true,
                            bool* ok = nullptr);

    virtual ~MessageBase() = default;
private:
    MessageBase() = default;
};

inline LX_BASE_EXPORT Base::MessageBase& Message()
{
    return Base::MessageBase::instance();
}

}  // namespace Base
