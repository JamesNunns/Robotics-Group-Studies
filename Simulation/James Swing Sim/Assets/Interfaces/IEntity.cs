using System.Collections.Generic;

namespace Interfaces
{
    /// <summary>
    /// Entity Interface for defining a generic entity class
    /// All algorithms should have defined entity classes inheriting from IEntity
    /// </summary>
    public interface IEntity
    {
        //Base class for all entities used in the simulation
        //Provides the function names independantly of python scripts, and performs type conversions

        /// <summary>
        /// Method called to trigger the neural net to perform an Action
        /// </summary>
        /// <param name="inputs">List of the inputs into the neural net</param>
        /// <param name="currReward">Reward value of the current state</param>
        /// <returns>Returns List of floats outputs, the output actions decided by the net</returns>
        List<float> DoAction(List<float> inputs, float currReward);
    }
}
