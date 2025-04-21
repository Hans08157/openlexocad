#pragma once

#include <Core/Variant.h>

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT Value
{
public:
    Value();
    virtual ~Value();
    virtual void setValue(const Core::Variant& aVariant);
    virtual bool isNull();
};

class LX_OPENLXAPP_EXPORT ValueInteger : public Value
{
public:
    ValueInteger();
    virtual ~ValueInteger();
    ValueInteger(const Core::Variant& aVariant);
    ValueInteger(int aValue);
    void setValue(const Core::Variant& aVariant) override;
    void setValue(int aValue);
    int getValue();
    bool isNull() override;

private:
    int _value;
    bool _isNull = true;
};

class LX_OPENLXAPP_EXPORT ValueDouble : public Value
{
public:
    ValueDouble();
    virtual ~ValueDouble();
    ValueDouble(const Core::Variant& aVariant);
    ValueDouble(double aValue);
    void setValue(const Core::Variant& aVariant) override;
    void setValue(double aValue);
    double getValue();
    bool isNull() override;

private:
    double _value;
    bool _isNull = true;
};
}  // namespace OpenLxApp
