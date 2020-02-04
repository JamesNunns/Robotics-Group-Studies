using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ankle : MonoBehaviour
{
	public float speed;

	private Rigidbody2D rb2d;

	private HingeJoint2D hinge;

	void Start()
	{
		rb2d = GetComponent<Rigidbody2D> ();
		hinge = GetComponent<HingeJoint2D> ();
	}

	void FixedUpdate()
	{
		float moveHorizontal = Input.GetAxis("Horizontal");
		if (Input.GetKey("z"))
		{
			rb2d.AddTorque(-500);
		}
		if (Input.GetKey("c"))
		{
			rb2d.AddTorque(500);
		}
		hinge.useLimits = true;
	}
}

