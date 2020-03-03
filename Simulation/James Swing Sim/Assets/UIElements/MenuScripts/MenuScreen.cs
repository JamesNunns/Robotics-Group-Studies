﻿using Interfaces;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

/// <summary>
/// Script powering all elements of the Main Menu
/// </summary>
public class MenuScreen : MonoBehaviour
{
    //Define Dropdowns, buttons, and gameobjects on the Unity end
    public Dropdown MethodDropdown;
    public Dropdown FitnessDropdown;
    public Button LaunchButton;
    public Button QuitButton;
    public GameObject spawner;
    public GameObject Swing;
    public InputField popInput;

    public GameObject MethodText;
    public GameObject GenText;

    //string path = @"..\James Swing Sim\Assets\PythonClasses";
    FitnessFunctions functions; //Class for holding all potential fitness functions

    InterfaceController interfaceController; //interface controller to hold all potential algorithm options

    int populationSize;

    public MethodsText MethodsText { get; set; }
    public GenerationText GenerationText { get; private set; }

    /// <summary>
    /// Finds all potential fitness function and algorithm options
    /// Generates Dropdown options list
    /// </summary>
    private void Start()
    {
        //Generate options for the fitness Dropdown
        functions = new FitnessFunctions();
        interfaceController = new InterfaceController();

        //TODO: Add the options to load from a file, should that file exist
        //TODO: Add quit button on other page, which saves the current state down to JSON file

        MethodDropdown.ClearOptions();
        FitnessDropdown.ClearOptions();

        //MethodDropdown = GameObject.Find("pySelectOptions").GetComponent<Dropdown>();
        foreach (string module in interfaceController.Modules)
        {
            MethodDropdown.options.Add(new Dropdown.OptionData(module)); //adds each module to the dropdown list
        }


        //FitnessDropdown = GameObject.Find("FitnessFuncOptions").GetComponent<Dropdown>();
        foreach (string f in functions.fitnessFunctionNames)
        {
            FitnessDropdown.options.Add(new Dropdown.OptionData(f));
        }

        MethodDropdown.RefreshShownValue();
        FitnessDropdown.RefreshShownValue();
    }

    /// <summary>
    /// Defines listeners for the LaunchSim and Quit buttons
    /// </summary>
    private void Awake()
    {
        LaunchButton.onClick.AddListener(new UnityEngine.Events.UnityAction(LaunchSim));
        QuitButton.onClick.AddListener(new UnityEngine.Events.UnityAction(QuitSim));
    }

    /// <summary>
    /// Method to quit the program
    /// </summary>
    private void QuitSim()
    {
        Application.Quit();
    }

    /// <summary>
    /// Collect chosen algorithm, fitness function, and population
    /// Loads and initialises the testing Scene
    /// </summary>
    private void LaunchSim()
    {
        string methodString = interfaceController.Modules[MethodDropdown.value];
        FitnessFunctions.FitnessFunctionDelegate fitnessMethod = functions.GetfitnessFunction(functions.fitnessFunctionNames[FitnessDropdown.value]);
        if (popInput.text != null)
        {
            populationSize = int.Parse(popInput.text);
        }
        else
        {
            populationSize = 0;
        }
        Vector3 position = new Vector3
        {
            x = 0,
            y = 0,
            z = 0
        };
        GameObject newSpawner = Instantiate(spawner, position, new Quaternion());
        SpawnSwing swingSpawnScript = newSpawner.AddComponent<SpawnSwing>();
        swingSpawnScript.Construct(methodString, newSpawner, Swing, fitnessMethod, populationSize);

        GameObject NewMethodText = Instantiate(MethodText);
        MethodsText MText = NewMethodText.AddComponent<MethodsText>();
        MText.Construct(swingSpawnScript, NewMethodText.GetComponent<Text>());

        GameObject NewGenText = Instantiate(GenText);
        GenerationText GenerText = NewGenText.AddComponent<GenerationText>();
        GenerText.Construct(swingSpawnScript, NewMethodText.GetComponent<Text>());

        DontDestroyOnLoad(newSpawner);
        DontDestroyOnLoad(NewMethodText);
        DontDestroyOnLoad(NewGenText);

        SceneManager.LoadScene("SwingSim", LoadSceneMode.Single);
    }
}

