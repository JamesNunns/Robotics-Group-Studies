using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lock : MonoBehaviour
{
	// Create variables of all of the individual pieces of the body
	private Rigidbody2D leg;

	private Rigidbody2D foot;

	private Rigidbody2D torso;

	private Rigidbody2D head;

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
        head = GameObject.Find("Head").GetComponent<Rigidbody2D>();
        thigh = GameObject.Find("Thigh").GetComponent<Rigidbody2D>();
        upperarm = GameObject.Find("Upperarm").GetComponent<Rigidbody2D>();
        forearm = GameObject.Find("Forearm").GetComponent<Rigidbody2D>();

    }
    // Define a locking function
    private void locking()
    {
    	leg.freezeRotation = true;
    	foot.freezeRotation = true;
    	torso.freezeRotation = true;
    	head.freezeRotation = true;
    	thigh.freezeRotation = true;
    	upperarm.freezeRotation = true;
    	forearm.freezeRotation = true;
    }
    // Update is called once per frame
    void Update()
    {
    	if (Input.GetKey("m"))
    	{
    		locking();
    	}
        
    }
}
