using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Linq;
using System;

public class CustomRotationLeft : MonoBehaviour
/// <summary>
/// This class controls the movement of the simulation
/// and attempts to replicate Nao's interface closely.
///<\summary>
{
	/// Define all the joints that can move
	HingeJoint leftShoulder;

	HingeJoint leftElbow;

	HingeJoint leftKnee;

	HingeJoint leftAnkle;

	HingeJoint leftHip;

	/// Have a limiting angle for each joint
	float leftShoulderAngle;

	float leftElbowAngle;

	float leftKneeAngle;

	float leftAnkleAngle;

	float leftHipAngle;

	
	/// List every joint and angle together
	List<HingeJoint> allJoints = new List<HingeJoint>();
	List<float> allAngles = new List<float>();

	Dictionary<HingeJoint, float> low_cm = new Dictionary<HingeJoint, float>();
	Dictionary<HingeJoint, float> high_cm = new Dictionary<HingeJoint, float>();

	void Start()
	{
		/// Assign all of the defined joints to the correct game objects
		leftShoulder = GameObject.Find("LeftBicep").GetComponent<HingeJoint>();

		leftElbow = GameObject.Find("LeftForearm").GetComponent<HingeJoint>();

		leftKnee = GameObject.Find("LeftShin").GetComponent<HingeJoint>();

		leftAnkle = GameObject.Find("LeftFoot").GetComponent<HingeJoint>();

		leftHip = GameObject.Find("LeftThigh").GetComponent<HingeJoint>();


		/// Set all the starting angles to 0
		leftShoulderAngle = 0;
		leftElbowAngle = 0;
		leftKneeAngle = 0;
		leftAnkleAngle = 0;
		leftHipAngle = 0;

		/// Populate the lists with the correct HingeJoint objects
		
		allJoints.Add(leftShoulder);
		allJoints.Add(leftElbow);
		allJoints.Add(leftKnee);
		allJoints.Add(leftAnkle);
		allJoints.Add(leftHip);

		allAngles.Add(leftShoulderAngle);
		allAngles.Add(leftElbowAngle);
		allAngles.Add(leftKneeAngle);
		allAngles.Add(leftAnkleAngle);
		allAngles.Add(leftHipAngle);

		low_cm.Add(leftElbow, Mathf.Rad2Deg*(0.050664f));
		low_cm.Add(leftShoulder, Mathf.Rad2Deg*(0.995608f));
		low_cm.Add(leftKnee, Mathf.Rad2Deg*(1.56f));
		low_cm.Add(leftAnkle, Mathf.Rad2Deg*(0.921976f));
		low_cm.Add(leftHip, Mathf.Rad2Deg*(-0.052198f));

		high_cm.Add(leftElbow, Mathf.Rad2Deg*(1.356098f));
		high_cm.Add(leftShoulder, Mathf.Rad2Deg*(1.322266f));
		high_cm.Add(leftKnee, Mathf.Rad2Deg*(-0.092082f));
		high_cm.Add(leftAnkle, Mathf.Rad2Deg*(-1.141338f));
		high_cm.Add(leftHip, Mathf.Rad2Deg*(-1.5708f));
	}

	void Move(HingeJoint joint, float ang, float speed)
	/// <summary>
	/// This class moves a single joint to the passed angle
	/// at a specified speed. The angles are defined in the
	/// same way as in the Nao interface. Speed will also be,
	/// but currently is not.
	/// <\summary>
	{   
		/// direction sets motion to be clockwise or anti
		float direction = 1;

		/// Some angles have to be changed because of how
		/// Nao defines its angles
		/// Also, set the speed to be in degrees per second
		if (joint == leftShoulder)
		{
			ang += 40;
			speed *= 246;
		}
		else if (joint == leftElbow)
		{
			ang *= -1;
			ang = 180 - ang;
			speed *= 246;
		}
		else if (joint == leftHip)
		{
			ang = 180 + ang;
			speed *= 378;
		}
		else if (joint == leftAnkle)
		{
			ang *= -1;
			ang = 90 - ang;
			speed *= 378;
		}
		else
		{
			speed *= 378;
		}
		for (int i = 0; i < 5; i++)
		/// Set the angle in the list allAngles to the correct limit angle
		{
			if (joint == allJoints[i])
			{
				allAngles[i] = ang;
			}
		}	
		/// Turn off joint limits temporarily
		joint.useLimits = false;
		/// Define a motor for the joint
		JointMotor motor = joint.motor;
		if (ang < joint.angle + 90)
		/// Determine direction of rotation
			{
				direction = -1;
			}
		/// Set the motor velocity, and switch the motor on
		motor.targetVelocity = speed*direction;
		joint.motor = motor;
		joint.useMotor = true;

	}

	void changePosition(Dictionary<HingeJoint, float> position, float speed)
	{
		for (int i = 0; i < 5; i++)
		{
			allJoints[i].useLimits = false;
		}
		foreach (KeyValuePair<HingeJoint, float> item in position)
		{
			Move(item.Key, item.Value, speed);
		}

	}

	void Lock(HingeJoint joint)
	/// <summary>
	/// This method will lock the joint so it cannot rotate more than 1 degree each way
	/// <\summary>
	{
		/// Define the joint's motor and set its velocity to zero, then switch it on
		JointMotor motor = joint.motor;
		motor.targetVelocity = 0;
		joint.motor = motor;
		joint.useMotor = true;

		/// Find the corresponding angle of the joints and set its limmits to +-1 of that angle
		int ind = allJoints.IndexOf(joint);
		JointLimits limits = joint.limits;
		limits.min = allAngles[ind] -90.5f;
		limits.max = allAngles[ind] -89.5f;
		joint.limits = limits;
		joint.useLimits = true;
	}

	void Update()
	{
		/// These are test inputs, they can be changed
		if (Input.GetKey("m")) //stand
		{
			Move(leftKnee, 105, 1f);
			Move(leftElbow, -90, 1f);
			//Move(leftShoulder, 57, 1f);
			Move(leftHip, -100, 1f);
			Move(leftAnkle, 0, 1f);
		}
		if (Input.GetKey("n")) //crouch
		{
			Move(leftKnee, 260, 1f);
			Move(leftElbow, -170, 1f);
			//Move(leftShoulder, Mathf.Rad2Deg*(1.65f), 1f);
			Move(leftHip, -200, 1f);
			Move(leftAnkle, -95, 1f);
		}	
		if (Input.GetKey("p"))
		{
			changePosition(low_cm, 0.5f);
		}
		if (Input.GetKey("o"))
		{
			changePosition(high_cm, 0.5f);
		}
		if (Input.GetKey("y"))
		{
			SceneManager.LoadScene("SampleScene");
		}
		for (int i = 0; i < 5; i++)
		/// This will lock any joint that is within 1 degree of its limit angle
		{
			if (allAngles[i] < allJoints[i].angle + 95f && allAngles[i] > allJoints[i].angle + 85f)
			{
				Lock(allJoints[i]);
			}
		}

		
	}
}

