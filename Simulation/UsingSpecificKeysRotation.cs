using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotation : MonoBehaviour
{
    public float Torque;
    public KeyCode ClockwiseKey;
    public KeyCode AntiClockwiseKey;
    private Rigidbody2D rb2d;
    

    // Using for initialising
    void Start ()
    {
        rb2d = GetComponent<Rigidbody2D>();
       
    }

    // FixedUpdate is called once per frame

    void FixedUpdate ()
    {
        //float horz = Input.GetKeyDown(EnterKey);
  
        if (Input.GetKey(ClockwiseKey))
        {
            rb2d.AddTorque(Torque);
        }
        //if right arrow is pressed
        if (Input.GetKey(AntiClockwiseKey))
        {
            rb2d.AddTorque(-1 * Torque);
        }
         
    }
}
