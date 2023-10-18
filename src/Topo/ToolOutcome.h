#pragma once

namespace Topo
{
class LX_TOPO_EXPORT ToolOutcome
{
public:
    ToolOutcome() = default;
    ToolOutcome(bool okay):_okay(okay){};

    bool isOkay() { return _okay; };
    void setOkay(bool ok) { _okay = ok; };

private:
    bool _okay = false;
};
}