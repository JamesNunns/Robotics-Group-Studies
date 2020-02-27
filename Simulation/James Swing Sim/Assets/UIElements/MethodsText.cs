using UnityEngine;
using UnityEngine.UI;

public class MethodsText : MonoBehaviour
{
    public Text txt;
    public GameObject spawner;
    public SpawnSwing spawnController;
    // Start is called before the first frame update
    void Start()
    {
        spawner = GameObject.Find("SwingSpawner");
        spawnController = spawner.GetComponent<SpawnSwing>();
    }

    // Update is called once per frame
    void Update()
    {
        string fName = spawnController.generationController.FileName;
        txt.text = ("Method Used: " + fName.Remove(fName.Length - 3) + "@Fitness Function: " + spawnController.fitness.ToString()).Replace("@", System.Environment.NewLine).ToString();
    }
}
