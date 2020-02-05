using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Knee : MonoBehaviour
{

	private Rigidbody2D rb2d;

	private HingeJoint2D hinge;

	private Rigidbody2D leg;

	private JointMotor2D motor;

	void Start()
	{
		leg = GameObject.Find("Leg").GetComponent<Rigidbody2D>();
		rb2d = GetComponent<Rigidbody2D> ();
		hinge = GetComponent<HingeJoint2D> ();
		motor = hinge.motor;
	}

	public void NewAngle(float ang)
	{ 
		leg.freezeRotation = false;
		if (hinge.jointAngle > ang)
		{
			rb2d.AddTorque(500);
		}
		if (hinge.jointAngle <= ang)
		{
			leg.freezeRotation = true;
		}
	}

	public void NewAngle1(float ang)
	{ 
		leg.freezeRotation = false;
		if (hinge.jointAngle < ang)
		{
			rb2d.AddTorque(-500);
		}
		if (hinge.jointAngle >= ang)
		{
			leg.freezeRotation = true;
		}
	}

	void FixedUpdate()
	{
		if (Input.GetKey("a"))
		{
			rb2d.AddTorque(-50);
		}
		if (Input.GetKey("d"))
		{
			rb2d.AddTorque(50);
		}
		if (Input.GetKey("k"))
		{
			NewAngle(200);
		}
		if (Input.GetKey("l"))
		{
			NewAngle1(330);
		}
	}
}
