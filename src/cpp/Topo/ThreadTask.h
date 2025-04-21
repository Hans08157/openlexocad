#pragma once
#include <functional>

namespace Topo
{
class ShapeTool;

class ThreadTask
{
public:
    ThreadTask(){};
    virtual ~ThreadTask(){};
};

class MainThreadCallback
{
public:
    MainThreadCallback(){};
    virtual ~MainThreadCallback(){};
    virtual void operator()(int done_in_percent) const = 0;
};

class ThreadTaskWorker
{
public:
    ThreadTaskWorker(){};
    virtual ~ThreadTaskWorker(){};
    virtual void operator()(Topo::ThreadTask* runable) const = 0;
};

class ThreadPoolData
{
};

class ThreadPool
{
    friend Topo::ShapeTool;

public:
    virtual int idealThreadCount() = 0;
    virtual void runParallel(int threads,
                             const std::vector<Topo::ThreadTask*>&,
                             const Topo::ThreadTaskWorker& worker,
                             const Topo::MainThreadCallback& callback) = 0;

    virtual void startTask(std::function<void()> fun) = 0;
    virtual void stopAndJoinAllTasks() = 0;

protected:
    virtual ~ThreadPool(){};
    ThreadPool(){};
};
}  // namespace Topo