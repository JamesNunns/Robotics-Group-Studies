using Interfaces;
using System.Collections.Generic;

namespace PythonInterface.Interfaces
{
    public interface IGenerationController
    {
        IEntity MakeEntity();


        void NextGeneration(List<float> entityFitnesses, List<IEntity> Entities);
        
    }
}
