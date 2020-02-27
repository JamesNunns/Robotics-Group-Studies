using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace PythonInterface.Interfaces
{
    public class FitnessFunctions
    {
        //FitnessFunctions class aims to house all potential fitness functions, which then allows easy selection at runtime
        public delegate float FitnessFunctionDelegate(List<float> angles, List<float> velocities, List<float> actions);
        public List<FitnessFunctionDelegate> fitnessFunctionList = new List<FitnessFunctionDelegate>();

        public List<string> fitnessFunctionNames = new List<string>();

        FitnessFunctionDelegate findFitness;

        public FitnessFunctions()
        {
            //Tell class which methods are available fitness functions
            //To add more functions, first define the method, then append it to the list below
            FitnessFunctionDelegate exampleFunction = ExampleFitnessFunction;
            fitnessFunctionList.Add(exampleFunction);


            foreach (FitnessFunctionDelegate f in fitnessFunctionList)
            {
                fitnessFunctionNames.Add(f.ToString());
            }
        }
        public FitnessFunctionDelegate GetfitnessFunction(string fitnessFuncToUse)
        {
            //Easy method of allocating which function to use

            findFitness = fitnessFunctionList.Where(f => f.ToString() == fitnessFuncToUse).FirstOrDefault();
            return findFitness;
        }


        //TODO: Add proper fitness function

        public float ExampleFitnessFunction(List<float> angles, List<float> velocities, List<float> actions)
        {
            return (float)0;
        }


        //Add more fitness functions below:
    }
}
