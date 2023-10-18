#pragma once 

namespace Core
{
class LX_CORE_EXPORT Solvable
{
public:
    virtual ~Solvable() {}

    // Is called before execute(). Can be overriden to solve the relationships of an object and update properties in dependent objects.
    virtual void solve() = 0;

    void setIsSolvingEnabled(bool on);
    bool isSolvingEnabled() const;

    bool mustBeSolved() const;
    void setMustBeSolved(bool on);

private:
    bool _isSolvingEnabled = true;
    bool _mustBeSolved = false;
};

}  // namespace Core