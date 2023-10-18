#pragma once 

#include <map>

namespace App
{
class Element;
}

namespace Core
{
class DocObject;

struct ImportMessageDataType
{
    Core::DocObject* ImportedDocument;
    std::map<App::Element*, App::Element*> Original2copy;
};

}  // namespace Core
