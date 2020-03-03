using System.Collections.Generic;

namespace Interfaces
{
    /// <summary>
    /// Interface class to define a generic GenerationController
    /// </summary>
    public interface IGenerationController
    {
        /// <summary>
        /// Method called whenever a new swinger needs to be spawned
        /// </summary>
        /// <returns>new Entity object, of a class inheriting from IEntity</returns>
        IEntity MakeEntity();

        /// <summary>
        /// Method called to allow the algorithm to perform any needed operations between generations,
        /// such as selecting the best performing entities.
        /// </summary>
        /// <param name="entityFitnesses">List of final fitnesses for each entity</param>
        /// <param name="Entities">List of entities in the current generation</param>
        void NextGeneration(List<float> entityFitnesses, List<IEntity> Entities);

    }
}
