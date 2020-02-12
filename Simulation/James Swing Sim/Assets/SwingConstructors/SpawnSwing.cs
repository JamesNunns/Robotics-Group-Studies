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
    // Start is called before the first frame update
    void Start()
    {
        makeSwing(swingToMake);
    }

    void makeSwing(int swingsToMake)
    {
        spawner.transform.Translate(Vector3.left * swingSep * (int)(swingToMake / 2));
        for (int i = 0; i < swingsToMake; i++)
        {
            Instantiate(swing, position.position, position.rotation);
            spawner.transform.Translate(Vector3.right * swingSep);
        }
    }
}
