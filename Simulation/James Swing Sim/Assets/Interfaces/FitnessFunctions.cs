using System;
using System.Collections.Generic;
using System.Linq;

namespace Interfaces
{
    public class FitnessFunctions
    {
        //FitnessFunctions class aims to house all potential fitness functions, which then allows easy selection at runtime
        public delegate float FitnessFunctionDelegate(List<float> angles, List<float> velocities, List<float> actions, EntityController entityBrain);
        public List<FitnessFunctionDelegate> fitnessFunctionList = new List<FitnessFunctionDelegate>();

        public List<string> fitnessFunctionNames = new List<string>();

        //TODO: Add proper lengths and mass
        readonly float[] arrayLengths = { 1, (float)0.5, (float)0.2 };
        List<float> Lengths { get; set; }
        readonly float Mass = 5;

        readonly float EffortWeight = (float)0.01;

        FitnessFunctionDelegate findFitness;

        /// <summary>
        /// FitnessFunctions aims to house every possible fitness function selectable in the start menu.
        /// </summary>
        public FitnessFunctions()
        {
            Lengths = new List<float>(arrayLengths);
            //Tell class which methods are available fitness functions
            //To add more functions, first define the method, append the name to the list below, and then add an extra case in GetfitnessFunction()
            fitnessFunctionNames.Add("Example");
            fitnessFunctionNames.Add("StoredEnergy");
        }

        /// <summary>
        /// Method to retrieve the fitness function from it's string name
        /// </summary>
        /// <param name="fitnessFuncToUse">String name of the desired fitness function. Must be contained in fitnessFunctionNames.</param>
        /// <returns>FitnessFunction, the method chosen from the input string.</returns>
        public FitnessFunctionDelegate GetfitnessFunction(string fitnessFuncToUse)
        {
            //Easy method of allocating which function to use

            switch (fitnessFuncToUse)
            {
                case "Example":
                    findFitness = ExampleFitnessFunction;
                    break;
                case "StoredEnergy":
                    findFitness = EnergyConservation;
                    break;
                default:
                    findFitness = EnergyConservation;
                    break;
            }
            return findFitness;
        }

        /// <summary>
        /// Rough method to punish unnessesary actoins
        /// </summary>
        /// <param name="actions">List of the angular actions performed</param>
        /// <param name="entityBrain">The EntityController object, to track each effort individually</param>
        /// <returns>Returns Effort, value encoding the amount of motion performed</returns>
        public static float CurrentEffort(List<float> actions, EntityController entityBrain)
        {
            foreach (float a in actions)
            {
                entityBrain.Effort += (float)Math.Pow(a, 2);
            }
            return entityBrain.Effort;
        }

        /// <summary>
        /// Example fitness function, to test simulation
        /// </summary>
        /// <param name="angles">Swing input angles</param>
        /// <param name="velocities">Swing input velocities</param>
        /// <param name="actions">All actions taken by the AI in the last timestep</param>
        /// <returns>Reward value of the current state</returns>
        public static float ExampleFitnessFunction(List<float> angles, List<float> velocities, List<float> actions, EntityController entityBrain)
        {
            float reward = 0;
            foreach (float ang in angles)
            {
                reward += (float)Math.Pow(ang, 2);
            }
            return reward;

        }

        /// <summary>
        /// Fitness Function which calculates the total energy in the swing, and deducts the amount of effort performed in this state 
        /// </summary>
        /// <param name="angles">Current state angular positions</param>
        /// <param name="velocities">Current state velocities</param>
        /// <param name="actions">Actions performed by the AI</param>
        /// <param name="entityBrain">The EntityController object, to track each effort individually</param>
        /// <returns></returns>
        public float EnergyConservation(List<float> angles, List<float> velocities, List<float> actions, EntityController entityBrain)
        {
            float reward = 0;
            for (int i = 0; i < angles.Count(); i++)
            {
                double delH = Lengths[i] * (1 - Math.Cos(angles[i]));
                double v = Lengths[i] * velocities[i];
                reward += (float)(Mass * UnityEngine.Physics.gravity.magnitude * delH + 0.5 * Mass * Math.Pow(v, 2));
            }
            reward -= EffortWeight * CurrentEffort(actions, entityBrain);
            return reward;
        }

        //Add more fitness functions below:
    }
}
