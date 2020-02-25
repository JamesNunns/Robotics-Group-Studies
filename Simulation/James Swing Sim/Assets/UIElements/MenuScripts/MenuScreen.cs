using PythonInterface.Interfaces;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class MenuScreen : MonoBehaviour
{
    List<string> options;
#pragma warning disable CS0649 // Add readonly modifier

    //TODO: Use script to instantiate dropdowns to fix null reference pointers?
    public Dropdown MethodDropdown;
    public Dropdown FitnessDropdown;
    public Button LaunchButton;
    public Button QuitButton;
    public GameObject spawner;
    public GameObject Swing;

    //TODO: Change dictionaries to dedicated class system
    List<Dictionary<string, string>> methodParams;
#pragma warning restore CS0649 // Add readonly modifier

    Dictionary<string, string> deepQ = new Dictionary<string, string>();

    string path = @"..\James Swing Sim\Assets\PythonClasses";
    List<string> filesInPath;
    FitnessFunctions functions;
    public MenuScreen()
    {
        //Generate options for the Method Dropdown
        filesInPath = new List<string>(Directory.GetFiles(path).Where(f => !f.Contains(".meta"))); //finds all non .meta files in the directory given by path
        foreach (string fullFName in filesInPath)
        {
            MethodDropdown.options.Add(new Dropdown.OptionData(Path.GetFileNameWithoutExtension(fullFName))); //adds each file name without extensions to the dropdown options list
        }
        

        //Generate options for the fitness Dropdown
        functions = new FitnessFunctions();
        foreach (FitnessFunctions.FitnessFunctionDelegate f in functions.fitnessFunctionList)
        {
            FitnessDropdown.options.Add(new Dropdown.OptionData(f.ToString()));
        }


        //Define dictionary of args for RLController.py
        deepQ.Add("entityName", "Agent");
        deepQ.Add("controllerName", "Controller");
        deepQ.Add("thinkFN", "perform_action");
        deepQ.Add("genStepFN", "step");
        deepQ.Add("makeEntityFN", "make_agent");
        methodParams.Add(deepQ);

        //TODO: Add the options to load from a file, should that file exist
        //TODO: Add quit button on other page, which saves the current state down to JSON file


    }

    private void Awake()
    {
        LaunchButton.onClick.AddListener(new UnityEngine.Events.UnityAction(LaunchSim));
        QuitButton.onClick.AddListener(new UnityEngine.Events.UnityAction(QuitSim));
    }

    private void QuitSim()
    {
        Application.Quit();
    }

    private void LaunchSim()
    {
        string methodString = filesInPath[MethodDropdown.value];
        FitnessFunctions.FitnessFunctionDelegate fitnessMethod = functions.fitnessFunctionList[FitnessDropdown.value];
        GameObject newSpawner = Instantiate(spawner);

        Dictionary<string, string> paramDict = new Dictionary<string, string>(methodParams[MethodDropdown.value]);
        string controllerName = paramDict["controllerName"];
        string makeEntityName = paramDict["makeEntityFN"];
        string genStepFuncName = paramDict["genStepFN"];
        string entityName = paramDict["entityName"];
        string thinkFuncName = paramDict["thinkFN"];

        SpawnSwing swingSpawnScript = new SpawnSwing(methodString, path, newSpawner, Swing, fitnessMethod, controllerName, makeEntityName, genStepFuncName, entityName, thinkFuncName);
        DontDestroyOnLoad(newSpawner);
        //TODO: Load other scene
    }
}

public class methodGenerator
{
    public methodGenerator(string fileName, string controllerName, string makeEntityFn, string genStepFN, string entityName, string thinkFN)
    {

    }
}

