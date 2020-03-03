using Interfaces;
using System;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Script to control the swing spawning object
/// </summary>
public class SpawnSwing : MonoBehaviour
{
    public GameObject spawner;
    public GameObject swing;

    public float swingSep = 0.1f;
    public int swingToMake;
    public float Lifetime = 120f;
    public int generations = 0;

    public List<IEntity> entities = new List<IEntity>();
    public FitnessFunctions.FitnessFunctionDelegate fitness;
    public List<float> entityRewards;
    public List<dynamic> pyEntities;
    EntityController entity;
    public string Method;

    public IGenerationController generationController;
    private float elapsedTime = 0f;

    public int PopSize { get; private set; }

    /// <summary>
    /// Constructor for class
    /// </summary>
    /// <param name="method">String name for the "method" algorithm to be used</param>
    /// <param name="spawnObject">GameObject responsible for spawning the Swingers</param>
    /// <param name="Swing">Swing GameObject to be spawned</param>
    /// <param name="fitnessFuncToUse">Fitness function to be used when determining reward</param>
    /// <param name="PopulationSize">Total population of each generation</param>
    /// <param name="startGeneration">Generation to start at (when loading from a saved state)</param>
    /// <param name="startEntities">EntityControllers loaded from a saved state</param>
    public void Construct(string method, GameObject spawnObject, GameObject Swing, FitnessFunctions.FitnessFunctionDelegate fitnessFuncToUse, int PopulationSize, int startGeneration = 0, List<EntityController> startEntities = null)
    {
        fitness = fitnessFuncToUse;
        Method = method;
        int inputLength = Swing.transform.Find("Swing").gameObject.GetComponentsInChildren<HingeJoint2D>().Length * 2;
        int outputLength = Swing.transform.Find("Robot").gameObject.GetComponentsInChildren<HingeJoint2D>().Length;
        InterfaceController interfaceController = new InterfaceController(method, inputLength, outputLength);
        generationController = interfaceController.GetGenMethod();
        spawner = spawnObject;
        generations = startGeneration;
        if (startEntities != null)
        {
            foreach (EntityController e in startEntities)
            {
                entities.Add(e.swingAI);
            }
        }
        swing = Swing;
        PopSize = PopulationSize;
    }

    void Start()
    {
        MakeSwing(PopSize);
        generations += 1;
    }
    /// <summary>
    /// Cycles through creating and destroying generations
    /// </summary>

    void FixedUpdate()
    {
        spawner.transform.position = new Vector3 { x = 0, y = 0, z = 0 };
        if (elapsedTime >= Lifetime)
        {
            entityRewards = null;
            if (entities != null)
            {
                foreach (EntityController e in entities)
                {
                    entityRewards.Add(e.KillSelf());
                }
                generationController.NextGeneration(entityRewards, entities);
            }
            elapsedTime = 0f;

            MakeSwing(PopSize);
            generations += 1;
        }
        else
        {
            elapsedTime += Time.fixedDeltaTime;
        }
    }

    /// <summary>
    /// Creates all needed swing objects in a generation
    /// </summary>
    /// <param name="swingsToMake">Number of swing objects to make</param>
    void MakeSwing(int swingsToMake)
    {
        int fullSquare;
        int swingsLeft;
        int width = (int)Math.Sqrt(swingsToMake) + 1;
        spawner.transform.Translate(Vector3.left * swingSep * (int)(width / 2));
        spawner.transform.Translate(Vector3.down * swingSep * (int)(width / 2));  //Move to initial spawning position
        for (int i = 0; i < swingsToMake; i++)  //For each swing to be created
        {
            swingsLeft = swingsToMake - i;
            if (swingsLeft > width) //If row will be complete
            {
                for (int j = 0; j < width; j++)
                {
                    GameObject newSwing = Instantiate(swing, spawner.transform.position, spawner.transform.rotation);
                    if ((i + j >= entities.Count) | (entities == null))
                    {

                        entity = newSwing.AddComponent<EntityController>();
                        entity.Construct(newSwing, generationController.MakeEntity(), fitness);
                        entities.Add(entity.swingAI);
                    }
                    else
                    {
                        entity = newSwing.AddComponent<EntityController>();
                        entity.Construct(newSwing, entities[i + j], fitness);
                    }
                    spawner.transform.Translate(Vector3.right * swingSep);
                }
                spawner.transform.Translate(Vector3.left * swingSep * width);
                i += width - 1;
                spawner.transform.Translate(Vector3.up * swingSep);
            }
            else
            {
                for (int j = 0; j < swingsLeft; j++) //Finish an incomplete row
                {
                    GameObject newSwing = Instantiate(swing, spawner.transform.position, spawner.transform.rotation);
                    if ((i + j >= entities.Count) | (entities == null))
                    {

                        entity = newSwing.AddComponent<EntityController>();
                        entity.Construct(newSwing, generationController.MakeEntity(), fitness);
                        entities.Add(entity.swingAI);
                    }
                    else
                    {
                        entity = newSwing.AddComponent<EntityController>();
                        entity.Construct(newSwing, entities[i + j], fitness);
                    }
                    spawner.transform.Translate(Vector3.right * swingSep);
                }
                spawner.transform.Translate(Vector3.left * swingSep * swingsLeft);
                i += swingsLeft - 1;
                spawner.transform.Translate(Vector3.up * swingSep);
            }
        }
        int squareWidth = (int)Math.Pow(width, 2);
        if (squareWidth == swingsToMake)
        {
            fullSquare = 1;
        }
        else
        {
            fullSquare = 0;
        }
        spawner.transform.Translate(Vector3.down * swingSep * (int)(width / 2 - 1 + fullSquare));
        spawner.transform.Translate(Vector3.right * swingSep * (int)(width / 2));
    }
}
