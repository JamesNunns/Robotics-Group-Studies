using PythonInterface.Interfaces;
using System.Collections.Generic;

namespace Interfaces
{
    public class InterfaceController
    {
        IEntity entityToUse;
        IGenerationController generationControllerToUse;
        public List<string> modules { get; private set; }
        public InterfaceController()
        {
            modules.Add("deepQ");
        }

        public InterfaceController(string moduleToUse)
        {
            switch (moduleToUse)
            {
                case "deepQ":
                    break;
            }
        }
    }
}
