using Interfaces;
using System.Collections.Generic;

namespace PythonInterface.Interfaces
{
    public class GenericEntity : PythonBaseInterface
    {
        //Base class for all entities used in the simulation
        //Provides the function names independantly of python scripts, and performs type conversions

        delegate IronPython.Runtime.List ComputeActionDelegate(IronPython.Runtime.List inputs, float reward);
        readonly ComputeActionDelegate computeAction;
        public dynamic PyEntity { get; private set; }

        public GenericEntity(dynamic pyEntity, string thinkFunctionName, string path) : base(path)
        {
            /*Constructor for class. pyEntity is the entity object that gets returned when the python generation controller
            creates a new entity. thinkFunctionName provides the name within python of the function that "thinks" (provides an
            action given inputs), usually using the pyEntity neural net or Q table. */

            PyEntity = pyEntity;
            computeAction = op.GetMember(PyEntity, thinkFunctionName);
        }

        public List<float> DoAction(List<float> worldInputs, float currReward)
        {
            //Calls the python entity object to perform an action, based on the simulated inputs

            IronPython.Runtime.List pyInputs = new IronPython.Runtime.List();
            if (worldInputs != null)
            {
                foreach (float input in worldInputs)
                {
                    pyInputs.Add(input);
                }
            }

            IronPython.Runtime.List pyOutputs = computeAction(pyInputs, currReward);

            List<float> outputs = new List<float>();
            foreach (dynamic output in pyOutputs)
            {
                outputs.Add((float)output);
            }
            return outputs;
        }
    }
}
