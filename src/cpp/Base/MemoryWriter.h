#pragma once
#include <Base/Writer.h>
#include <map>


namespace Base
{
class Persistence;


class LX_BASE_EXPORT MemoryWriter : public AbstractWriter
{
public:
    MemoryWriter(const Base::String& FileName, int application_version, int document_version, int acis_document_version);
    virtual ~MemoryWriter();

    ConstIterator begin() const override { return FileList.begin(); }
    ConstIterator end() const override { return FileList.end(); }
    void addFile(const Base::String& Name, Base::Persistence* Object, const Base::String& Info = Base::String() ) override;
    void unsetFilenames() override;
    const std::vector<std::pair<Base::String, Base::String>> getFilenames() const override;
    const char* ind() override;
    void incInd() override;
    void decInd() override;
    bool saveInline() override { return false; };
    int get_application_version() const override;
    int get_document_version() const override;
    int get_acis_document_version() const override;
    void putNextEntry(const Base::String& entryName) override;
    void setComment(const std::string& comment) override;
    void setLevel(int level) override;
    void close() override;
    bool good() const override;

    void clear();
    bool writeToFile() override;

    std::ios_base::fmtflags flags() override;
    std::streamsize precision() override;
    char fill() override;
    int width() override;
    void fill(char) override;
    void width(int) override;
    void flags(std::ios_base::fmtflags fl) override;
    void precision(std::streamsize sz) override;
    uint64_t size() override;

    void appendWriter(std::shared_ptr<Base::AbstractWriter> p) override;
    void setCurrentEntry(const Base::String& entryName) override;
    void write(const char* s, std::streamsize sz) override;
    std::string getString();
    std::string getStringWithSubWriters();

    void addLargeFileToZip(const Base::String& entry, const Base::String& filename) override;


    void doWrite() override;

    template <typename T>
    friend Base::MemoryWriter& operator<<(Base::MemoryWriter& os, T& t)
    {                
        (*os._stream) << t;
        os.doWrite();                 
        return os;
    }

    template <typename T>
    friend Base::MemoryWriter& operator<<(Base::MemoryWriter& os, const T& t)
    {                
        (*os._stream) << t;
        os.doWrite();
        return os;
    }

    friend Base::MemoryWriter& operator<<(Base::MemoryWriter& os, std::ostream& (*pf)(std::ostream&))
    {
        (*os._stream) << pf;
        os.doWrite();
        return os;
    }



private:
    bool copyStreamToBuffer();
    bool copyStreamToBuffer(std::stringstream* stream, std::shared_ptr<std::vector<char>> buffer);
    void appendTo(Base::MemoryWriter& w);
    int _application_version;
    int _document_version;
    int _acis_document_version;
    Base::String _fileName;

    std::string _comment;
    int _level = 0;

    std::map <Base::String, std::pair<std::stringstream*, std::shared_ptr<std::vector<char>>>> _entries;
    std::vector<std::shared_ptr<Base::AbstractWriter>> _writer;
    std::shared_ptr<std::vector<char>> _buffer;
    std::vector<std::pair<Base::String, Base::String>> largeFiles;
    
    

};

}  // namespace Base
