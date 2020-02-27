
using Interfaces;
using System.Collections.Generic;

namespace PythonInterface.Interfaces
{
    public class GenericGenerationController : PythonBaseInterface
    {
        //Class for making the generation controller, which is the overarching tool to control the evolution of the AI across many generations
        public dynamic pyGenController { get; private set; }

        delegate List<float> processGenerationDelegate(IronPython.Runtime.List entityFitnesses, List<dynamic> pyEntities);
        delegate List<float> pyMakeEntityDelegate();

        readonly processGenerationDelegate processGeneration;
        readonly pyMakeEntityDelegate pyMakeEntity;

        readonly string FilePath;

        public string FileName { get; private set; }
        readonly string thinkFunctionName;
        readonly int inputLength;
        readonly int outputLength;


        public GenericGenerationController(string filePath, string FName, string pyGenControllerClassName, string processGenFunctionName, string makeEntityFunctionName, string pyEntityThinkFunctionName, int inputlength, int outputlength) : base(filePath + FName)
        {
            //Constructor needs the names (as strings) of the required classes and functions, so that it can load them as classes and methods in c#.
            pyGenController = scope.GetVariable(pyGenControllerClassName);
            processGeneration = op.GetMember(pyGenController, processGenFunctionName);
            pyMakeEntity = op.GetMember(pyGenController, makeEntityFunctionName);

            FilePath = filePath;
            FileName = FName;
            inputLength = inputlength;
            outputLength = outputlength;
            thinkFunctionName = pyEntityThinkFunctionName;
        }

        public GenericEntity MakeEntity()
        {
            //Method called whenever a new entity needs to be made. Creates the python entity object, and then wraps that into a genericEntity objetc.

            dynamic pyEntity = pyMakeEntity();
            GenericEntity newEntity = new GenericEntity(pyEntity, thinkFunctionName, FilePath);
            return newEntity;

        }

        public void NextGeneration(List<float> entityFitnesses, List<dynamic> pyEntities)
        {
            //Function to allow the python generation controller to perform actions between generations.
            //python generation controller needs to return itself at the end of these actions, in order to ensure the c# class is updated.

            IronPython.Runtime.List pyEntityFitnesses = new IronPython.Runtime.List();
            if (entityFitnesses != null)
            {
                foreach (float fitness in entityFitnesses)
                {
                    pyEntityFitnesses.Add(fitness);
                }
            }
            pyGenController = processGeneration(pyEntityFitnesses, pyEntities);
        }
    }
}
