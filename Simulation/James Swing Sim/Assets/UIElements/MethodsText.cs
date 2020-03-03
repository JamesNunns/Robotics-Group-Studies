using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// MethodsText controls the text describing selected method and fitness function
/// </summary>
public class MethodsText : MonoBehaviour
{
    public Text txt;
    public SpawnSwing spawnController;

    public void Construct(SpawnSwing spawner, Text TXT)
    {
        spawnController = spawner;
        txt = TXT;
    }


    /// <summary>
    /// Updates the text every call to FixedUpdate
    /// </summary>
    void FixedUpdate()
    {
        txt.text = ("Method Used: " + spawnController.Method + "@Fitness Function: " + nameof(spawnController.fitness)).Replace("@", System.Environment.NewLine).ToString();
    }
}
