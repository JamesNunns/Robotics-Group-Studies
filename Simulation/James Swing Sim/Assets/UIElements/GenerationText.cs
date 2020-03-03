using UnityEngine;
using UnityEngine.UI;

public class GenerationText : MonoBehaviour
{
    public Text txt;
    public SpawnSwing spawnController;

    public void Construct(SpawnSwing spawner, Text TXT)
    {
        spawnController = spawner;
        txt = TXT;
    }


    /// <summary>
    /// Uptades the text displaying generation number and current population
    /// </summary>
    // Update is called once per frame
    void FixedUpdate()
    {
        txt.text = ("Generations: " + spawnController.generations + "@Population: " + spawnController.PopSize).Replace("@", System.Environment.NewLine).ToString();
    }
}
