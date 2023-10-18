#pragma once

class static_object
{
public:
    static_object();
    virtual void cleanup() = 0;
};

class static_object_registry
{
public:
    static static_object_registry* instance();
    void add(static_object* obj);
    void cleanup();
private:
    std::set<static_object*> _objects;
};