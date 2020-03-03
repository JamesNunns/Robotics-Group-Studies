using Interfaces.Algorithms;
using System.Collections.Generic;

namespace Interfaces
{
    /// <summary>
    /// Class to control all potential algorithms
    /// </summary>
    public class InterfaceController
    {
        public IGenerationController generationControllerToUse;

        public List<string> Modules { get; private set; }

        /// <summary>
        /// Use this constructor to generate the List &lt; string &gt;  of algorithm options
        /// Do Module.Add(algorithmName) to define a new option
        /// </summary>
        public InterfaceController()
        {
            Modules = new List<string>
            {
                //"deepQ",
                "testExample"
            };
        }

        /// <summary>
        /// Use this constructor to generate the swing spawner
        /// Swing spawner object is InterfaceController.generationControllerToUse
        /// </summary>
        /// <param name="moduleToUse">Name of the chosen module. Will be an element of the Modules List, defined above</param>
        /// <param name="inputlength">Number of available inputs to the neural net</param>
        /// <param name="outputlength">Number of expected output options the net can take</param>
        public InterfaceController(string moduleToUse, int inputlength, int outputlength)
        {
            switch (moduleToUse)
            {
                case "deepQ":
                    break;

                case "testExample":
                    generationControllerToUse = new TestController(inputlength, outputlength);
                    break;

                default:
                    generationControllerToUse = new TestController(inputlength, outputlength);
                    break;
            }
        }

        public IGenerationController GetGenMethod()
        {
            return generationControllerToUse;
        }
    }
}
