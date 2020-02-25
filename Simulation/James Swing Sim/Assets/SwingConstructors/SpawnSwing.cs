using PythonInterface.Interfaces;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpawnSwing : MonoBehaviour
{
    public GameObject spawner;
    public GameObject swing;

    public Transform position;
    public float swingSep;
    public int swingToMake;
    public float Lifetime;
    public int generations;
    public string filePath;

    public List<EntityController> entities;
    public FitnessFunctions.FitnessFunctionDelegate fitness;
    public List<float> entityRewards;
    public List<dynamic> pyEntities;
    EntityController entity;

    public GenericGenerationController generationController;
    public SpawnSwing(string methodFile, string path, GameObject spawnObject, GameObject Swing, FitnessFunctions.FitnessFunctionDelegate fitnessFuncToUse, string controllerName, string makeEntityName, string genStepFuncName, string entityName, string thinkFuncName, int startGeneration = 0, List<EntityController> startEntities = null)
    {
        fitness = fitnessFuncToUse;
        EntityController testSwing = new EntityController(Swing, null, fitness);
        filePath = path + methodFile;
        generationController = new GenericGenerationController(path, methodFile, controllerName, genStepFuncName, makeEntityName, thinkFuncName, testSwing.inputLength, testSwing.outputLength);
        spawner = spawnObject;
        generations = startGeneration;
        entities = startEntities;
        swing = Swing;
    }


    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(Cycle());

        //MLMethod = ai.Methods.Where(f => f.ToString() == MethodToUse).FirstOrDefault();
    }
    IEnumerator Cycle()
    {
        while (true)
        {
            //TODO: make this flexible with an entitiesLeftToAdd int to take into account varying sizes of the input population when loading from a save
            if (entities is null)
            {
                MakeSwing(swingToMake);
                generations += 1;
            }
            yield return new WaitForSeconds(Lifetime);
            entityRewards = null;
            pyEntities = null;
            foreach (EntityController e in entities)
            {
                entityRewards.Add(e.KillSelf());
                dynamic currPyEntity = e.swingAI.PyEntity;
                pyEntities.Add(currPyEntity);
            }
            generationController.NextGeneration(entityRewards, pyEntities);
        }
    }

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
                    GameObject newSwing = Instantiate(swing, position.position, position.rotation);
                    entity = new EntityController(newSwing, generationController.MakeEntity(), fitness);
                    entities.Add(entity);
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
                    GameObject newSwing = Instantiate(swing, position.position, position.rotation);
                    entity = new EntityController(newSwing, generationController.MakeEntity(), fitness);
                    entities.Add(entity);
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
