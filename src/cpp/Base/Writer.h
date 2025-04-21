#pragma once
#include <Base/String.h>
#include <ostream>
#include <vector>

namespace Base
{
class Persistence;
class GlobalSave;
class GlobalAttachment;

class LX_BASE_EXPORT AbstractWriter
{
protected:
    struct FileEntry
    {
        Base::String FileName;
        Base::Persistence* Object;
    };

public:
    /// opens the file and write the first file
    AbstractWriter()
        : indent(0)
        , _globalSave(0)
        , _stream(0){

          };

    virtual ~AbstractWriter() = default;

    typedef std::vector<FileEntry>::const_iterator ConstIterator;
    virtual ConstIterator begin(void) const = 0;
    virtual ConstIterator end(void) const = 0;
    virtual void addFile(const Base::String& Name, Base::Persistence* Object, const Base::String& Info = Base::String()) = 0;
    virtual void unsetFilenames() = 0;
    virtual const std::vector<std::pair<Base::String, Base::String>> getFilenames() const = 0;
    virtual const char* ind(void) = 0;
    virtual void incInd(void) = 0;
    virtual void decInd(void) = 0;
    virtual bool saveInline() = 0;

    virtual void set_GlobalSave(Base::GlobalSave* p) { _globalSave = p; };
    virtual Base::GlobalSave* get_GlobalSave() { return _globalSave; };

    virtual int get_application_version() const = 0;
    virtual int get_document_version() const = 0;
    virtual int get_acis_document_version() const = 0;

    virtual void putNextEntry(const Base::String& entryName) = 0;

    virtual std::ios_base::fmtflags flags() = 0;
    virtual std::streamsize precision() = 0;
    virtual char fill() = 0;
    virtual int width() = 0;
    virtual void fill(char) = 0;
    virtual void width(int) = 0;
    virtual void flags(std::ios_base::fmtflags fl) = 0;
    virtual void precision(std::streamsize sz) = 0;
    virtual bool good() const = 0;
    virtual void close(){};
    virtual bool writeToFile() { return true; };
    virtual uint64_t size() { return 0; }
    virtual void write(const char* s, std::streamsize sz) = 0;
    virtual void doWrite(){};

    template <typename T>
    friend Base::AbstractWriter& operator<<(Base::AbstractWriter& os, T& t)
    {
        (*os._stream) << t;
        os.doWrite();
        return os;
    }

    template <typename T>
    friend Base::AbstractWriter& operator<<(Base::AbstractWriter& os, const T& t)
    {
        (*os._stream) << t;
        os.doWrite();
        return os;
    }

    friend Base::AbstractWriter& operator<<(Base::AbstractWriter& os, std::ostream& (*pf)(std::ostream&))
    {
        (*os._stream) << pf;
        os.doWrite();
        return os;
    }


    virtual void setComment(const std::string& comment) = 0;
    virtual void setLevel(int level) = 0;

    virtual void appendWriter(std::shared_ptr<Base::AbstractWriter> /*p*/){};
    virtual void setCurrentEntry(const Base::String& /*entryName*/){};

    virtual void addLargeFileToZip(const Base::String& entry, const Base::String& filename) = 0;



protected:
    std::vector<FileEntry> FileList;
    std::vector<std::pair<Base::String, Base::String>> FileNames;

    short indent;
    Base::GlobalSave* _globalSave;
    std::ostream* _stream;
};


class LX_BASE_EXPORT Writer : public AbstractWriter
{
public:
    Writer(const Base::String& FileName, int application_version, int document_version, int acis_document_version);
    ~Writer();

    ConstIterator begin(void) const override { return FileList.begin(); };
    ConstIterator end(void) const override { return FileList.end(); };
    void addFile(const Base::String& Name, Base::Persistence* Object, const Base::String& Info = Base::String()) override;
    void unsetFilenames() override;
    const std::vector<std::pair<Base::String, Base::String>> getFilenames() const override;
    const char* ind(void) override;
    void incInd(void) override;
    void decInd(void) override;
    bool saveInline() override { return false; };
    int get_application_version() const override;
    int get_document_version() const override;
    int get_acis_document_version() const override;
    void putNextEntry(const Base::String& entryName) override;
    void setComment(const std::string& comment) override;
    void setLevel(int level) override;
    // std::ostream * getStream();
    void close() override;
    bool good() const override;

    std::ios_base::fmtflags flags() override;
    std::streamsize precision() override;
    char fill() override;
    int width() override;
    void fill(char) override;
    void width(int) override;
    void flags(std::ios_base::fmtflags fl) override;
    void precision(std::streamsize sz) override;
    void write(const char* s, std::streamsize sz) override;
    void addLargeFileToZip(const Base::String& entry, const Base::String& filename) override
    {
        (void)entry;
        (void)filename;
    };

private:
    int _application_version;
    int _document_version;
    int _acis_document_version;
};


class LX_BASE_EXPORT Stream : public AbstractWriter
{
public:
    Stream(std::ostream& os);
    ~Stream();

    void setSaveInline(bool onoff);
    ConstIterator begin(void) const override { return FileList.begin(); }
    ConstIterator end(void) const override { return FileList.end(); }
    void addFile(const Base::String& Name, Base::Persistence* Object, const Base::String& Info = Base::String()) override;
    void unsetFilenames() override;
    const std::vector<std::pair<Base::String, Base::String>> getFilenames() const override;
    const char* ind(void) override;
    void incInd(void) override;
    void decInd(void) override;
    bool saveInline() override;
    int get_application_version() const override { return 1; };
    int get_document_version() const override { return 1; };
    int get_acis_document_version() const override { return 1; };
    void putNextEntry(const Base::String& entryName) override;
    void setComment(const std::string& comment) override;
    void setLevel(int level) override;
    void close() override;
    bool good() const override;

    std::ios_base::fmtflags flags() override;
    std::streamsize precision() override;
    char fill() override;
    int width() override;
    void fill(char) override;
    void width(int) override;
    void flags(std::ios_base::fmtflags fl) override;
    void precision(std::streamsize sz) override;
    void write(const char* s, std::streamsize sz) override;
    void addLargeFileToZip(const Base::String& entry, const Base::String& filename) override
    {
        (void)entry;
        (void)filename;
    }

private:
    bool _saveInline;
};



class Reader
{
public:
    Reader(std::istream* is, const Base::String& filename, const Base::String& fileInfo, Base::GlobalAttachment* ga)
        : _stream(is), _filename(filename), _fileInfo(fileInfo), _globalAttachment(ga){};

    std::istream* getStream() { return _stream; }
    Base::String getFilename() { return _filename; }
    Base::String getFileInfo() { return _fileInfo; }
    Base::GlobalAttachment* getGlobalAttachment() { return _globalAttachment; }

private:
    std::istream* _stream;
    Base::String _filename;
    Base::String _fileInfo;
    Base::GlobalAttachment* _globalAttachment;
};

}  // namespace Base
