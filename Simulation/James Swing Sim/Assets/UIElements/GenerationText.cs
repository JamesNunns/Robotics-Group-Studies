using UnityEngine;
using UnityEngine.UI;

public class GenerationText : MonoBehaviour
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
        txt.text = ("Generations: " + spawnController.generations + "@Population: " + spawnController.swingToMake).Replace("@", System.Environment.NewLine).ToString();
    }
}
