using System;
using System.Collections.Generic;

namespace Interfaces.Algorithms
{
    /// <summary>
    /// Example entity class for testing purposes.
    /// WILL NOT LEARN
    /// </summary>
    class TestEntity : IEntity
    {
        readonly Random random = new Random();

        public TestEntity()
        {

        }

        /// <summary>
        /// Example DoAction function
        /// </summary>
        public List<float> DoAction(List<float> inputs, float currReward)
        {
            List<float> outputs = new List<float>();
            for (int i = 0; i < inputs.Count; i++)
            {
                outputs.Add((float)random.NextDouble());
            }
            return outputs;
        }
    }

    /// <summary>
    /// Example generationController for testing purposes
    /// WILL NOT LEARN
    /// </summary>
    class TestController : IGenerationController
    {
        public TestController(int inputLength, int outputLength)
        {
            _ = inputLength + outputLength;
        }
        public IEntity MakeEntity()
        {
            return new TestEntity();
        }

        public void NextGeneration(List<float> entityFitnesses, List<IEntity> Entities)
        {
            Console.WriteLine("Generation Processed.");
        }
    }
}
