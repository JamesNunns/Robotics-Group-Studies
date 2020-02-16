using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Unlock : MonoBehaviour
{
	// Create variables of all of the individual pieces of the body
	private Rigidbody2D leg;

	private Rigidbody2D foot;

	private Rigidbody2D torso;

	private Rigidbody2D thigh;

	private Rigidbody2D upperarm;

	private Rigidbody2D forearm;
    // Start is called before the first frame update
    void Start()

    // Call each of the body parts
    {
        leg = GameObject.Find("Leg").GetComponent<Rigidbody2D>();
        foot = GameObject.Find("Foot").GetComponent<Rigidbody2D>();
        torso = GameObject.Find("Torso").GetComponent<Rigidbody2D>();
        thigh = GameObject.Find("Thigh").GetComponent<Rigidbody2D>();
        upperarm = GameObject.Find("UpperArm").GetComponent<Rigidbody2D>();
        forearm = GameObject.Find("Forearm").GetComponent<Rigidbody2D>();

    }
    // Define a locking function
    private void locking()
    {
    	leg.freezeRotation = false;
    	foot.freezeRotation = false;
    	torso.freezeRotation = false;
    	thigh.freezeRotation = false;
    	upperarm.freezeRotation = false;
    	forearm.freezeRotation = false;
    }
    // Update is called once per frame
    void Update()
    {
    	if (Input.GetKey("n"))
    	{
    		locking();
    	}
        
    }
}
