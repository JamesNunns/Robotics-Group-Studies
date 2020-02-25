using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace Interfaces
{
    public class PythonBaseInterface
    {
        //Base interface for using a python file in c# given a filepath
        public ScriptEngine engine { get; private set; }
        public ScriptSource source { get; private set; }
        public ScriptScope scope { get; private set; }
        public ObjectOperations op { get; private set; }
        public PythonBaseInterface(string filePath)
        {
            engine = Python.CreateEngine();
            source = engine.CreateScriptSourceFromFile(filePath);
            scope = engine.CreateScope();
            source.Execute(scope);
            op = engine.Operations;
        }

    }
}
