using Interfaces;
using System.Collections.Generic;

namespace PythonInterface.Interfaces
{
    public interface IEntity
    {
        //Base class for all entities used in the simulation
        //Provides the function names independantly of python scripts, and performs type conversions

        List<float> DoAction(List<float> inputs, float currReward);
    }
}
