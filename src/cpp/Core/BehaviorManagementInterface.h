
/**
 * @file
 * CBehaviorManagementInterface class declaration.
 *
 */
#pragma once

#include <Core/AbstractBehaviorMode.h>


namespace Core
{
class CAbstractBehaviorMode;

/**
 *
 *
 */
class CBehaviorManagementInterface
{
public:
    virtual Core::CAbstractBehaviorMode* setMode(Base::Type type, const Core::BehaviorAttributeMap& attributes) = 0;
    virtual Core::CAbstractBehaviorMode* getMode(void) const = 0;
};

}  // namespace Core
