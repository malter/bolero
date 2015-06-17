#pragma once
#include <string>
#include <vector>

#ifdef NO_TR1
    #include <memory>
    using std::shared_ptr;
#else
    #include <tr1/memory>
    using std::tr1::shared_ptr;
#endif

// TODO to allow calling functions/methods with arbitrary arguments we must
// create a callable object and pass a Python argument list


namespace bolero { namespace bl_loader {

struct ObjectState;
struct FunctionState;
struct MethodState;
struct ModuleState;
struct ListBuilderState;
class Object;
class Function;
class Method;
class Module;
class ListBuilder;

class PythonInterpreter
{
    shared_ptr<Module> currentModule;

    PythonInterpreter();
public:
    ~PythonInterpreter();
    static const PythonInterpreter& instance();

    void addToPythonpath(const std::string& path) const;
    shared_ptr<Module> import(const std::string& name) const;
    shared_ptr<ListBuilder> listBuilder() const;
};

enum CppType
{
    INT, DOUBLE, BOOL, STRING, ONEDARRAY, OBJECT
};

class Object
{
    friend PythonInterpreter;
public:
    shared_ptr<ObjectState> state;

    Object(shared_ptr<ObjectState> state);
    Method& method(const std::string& name);
    shared_ptr<std::vector<double> > as1dArray();
    double asDouble();
    int asInt();
    bool asBool();
    std::string asString();
};

// TODO Function and Method may contain duplicate code
class Function
{
    friend PythonInterpreter;
public:
    shared_ptr<FunctionState> state;

    Function(ModuleState& module, const std::string& name);
    Function& pass(CppType type);
    Function& call(...);
    shared_ptr<Object> returnObject();
};

class Method
{
    friend PythonInterpreter;
public:
    shared_ptr<MethodState> state;

    Method(ObjectState& object, const std::string& name);
    Method& pass(CppType type);
    Method& call(...);
    shared_ptr<Object> returnObject();
};

class Module
{
    friend PythonInterpreter;
public:
    shared_ptr<ModuleState> state;

    Module(const std::string& name);
    Function& function(const std::string& name);
    Object& variable(const std::string& name);
};

class ListBuilder
{
    friend PythonInterpreter;
public:
    shared_ptr<ListBuilderState> state;

    // WARNING: should not be used, use PythonInterpreter::listBuilder instead!
    ListBuilder();
    ListBuilder& pass(CppType type);
    shared_ptr<Object> build(...);
};

} } // End of namespace bolero::bl_loader
