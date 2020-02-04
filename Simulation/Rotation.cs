using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotation : MonoBehaviour
{
    public float Torque;
    private Rigidbody2D rb2d;
    private float negTorque;

    // Using for initialising
    void Start ()
    {
        rb2d = GetComponent<Rigidbody2D>();
       
    }

    // FixedUpdate is called once per frame

    void FixedUpdate ()
    {
        float horz = Input.GetAxis("Horizontal");
        //if right arrow is pressed
        if (horz > 0)
        {
            rb2d.AddTorque(horz * Torque);
        }
        if (horz < 0) //if left arrow is pressed
        {
            rb2d.AddTorque(horz * Torque);
        }
    }
}
