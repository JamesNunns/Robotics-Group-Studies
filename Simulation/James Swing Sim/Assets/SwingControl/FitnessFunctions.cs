using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace PythonInterface.Interfaces
{
    public class FitnessFunctions
    {
        //FitnessFunctions class aims to house all potential fitness functions, which then allows easy selection at runtime
        public delegate float FitnessFunctionDelegate(GameObject swing, EntityController entity);
        public List<FitnessFunctionDelegate> fitnessFunctionList;

        //TODO: Add proper fitness function

        public float ExampleFitnessFunction(GameObject swing, EntityController entity)
        {
            return (float)0;
        }

        public List<string> fitnessFunctionNames;

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
    }
}
