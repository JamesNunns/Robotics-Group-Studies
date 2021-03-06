using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Linq;
using System;

public class CustomRotationRight : MonoBehaviour
/// <summary>
/// This class controls the movement of the simulation
/// and attempts to replicate Nao's interface closely.
///<\summary>
{
	/// Define all the joints that can move
	HingeJoint rightShoulder;

	HingeJoint rightElbow;

	HingeJoint rightKnee;

	HingeJoint rightAnkle;

	HingeJoint rightHip;

	HingeJoint Neck;

	/// Have a limiting angle for each joint
	float rightShoulderAngle;

	float rightElbowAngle;

	float rightKneeAngle;

	float rightAnkleAngle;

	float rightHipAngle;

	float neckAngle;
	
	/// List every joint and angle together
	List<HingeJoint> allJoints = new List<HingeJoint>();
	List<float> allAngles = new List<float>();

	Dictionary<HingeJoint, float> low_cm = new Dictionary<HingeJoint, float>();
	Dictionary<HingeJoint, float> high_cm= new Dictionary<HingeJoint, float>();



	void Start()
	{
		/// Assign all of the defined joints to the correct game objects
		rightShoulder = GameObject.Find("RightBicep").GetComponent<HingeJoint>();

		rightElbow = GameObject.Find("RightForearm").GetComponent<HingeJoint>();

		rightKnee = GameObject.Find("RightShin").GetComponent<HingeJoint>();

		rightAnkle = GameObject.Find("RightFoot").GetComponent<HingeJoint>();

		rightHip = GameObject.Find("RightThigh").GetComponent<HingeJoint>();

		Neck = GameObject.Find("Body").GetComponent<HingeJoint>();

		/// Set all the starting angles to 0
		rightShoulderAngle = 0;
		rightElbowAngle = 0;
		rightKneeAngle = 0;
		rightAnkleAngle = 0;
		rightHipAngle = 0;
		neckAngle = 0;

		/// Populate the lists with the correct HingeJoint objects
		
		allJoints.Add(rightShoulder);
		allJoints.Add(rightElbow);
		allJoints.Add(rightKnee);
		allJoints.Add(rightAnkle);
		allJoints.Add(rightHip);
		allJoints.Add(Neck);

		allAngles.Add(rightShoulderAngle);
		allAngles.Add(rightElbowAngle);
		allAngles.Add(rightKneeAngle);
		allAngles.Add(rightAnkleAngle);
		allAngles.Add(rightHipAngle);
		allAngles.Add(neckAngle);

		low_cm.Add(rightElbow, Mathf.Rad2Deg*(0.050664f));
		low_cm.Add(rightShoulder, Mathf.Rad2Deg*(0.995608f));
		low_cm.Add(rightKnee, Mathf.Rad2Deg*(1.56f));
		low_cm.Add(rightAnkle, Mathf.Rad2Deg*(0.921976f));
		low_cm.Add(rightHip, Mathf.Rad2Deg*(-0.052198f));
		low_cm.Add(Neck, Mathf.Rad2Deg*(-0.671952f));

		high_cm.Add(rightElbow, Mathf.Rad2Deg*(1.356098f));
		high_cm.Add(rightShoulder, Mathf.Rad2Deg*(1.322266f));
		high_cm.Add(rightKnee, Mathf.Rad2Deg*(-0.092082f));
		high_cm.Add(rightAnkle, Mathf.Rad2Deg*(-1.141338f));
		high_cm.Add(rightHip, Mathf.Rad2Deg*(-1.5708f));
		high_cm.Add(Neck, Mathf.Rad2Deg*(0.253068f));

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
		if (joint == rightShoulder)
		{
			ang += 40;
			speed *= 246;
		}
		else if (joint == rightElbow)
		{
			ang *= -1;
			ang = 180 - ang;
			speed *= 246;
		}
		else if (joint == rightHip)
		{
			ang = 180 + ang;
			speed *= 378;
		}
		else if (joint == rightAnkle)
		{
			ang *= -1;
			ang = 90 - ang;
			speed *= 378;
		}
		else if (joint == Neck)
		{
			ang *= -1;
			ang += 90;
			speed *= 246;
		}
		else
		{
			speed *= 378;
		}
		for (int i = 0; i < 6; i++)
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
		for (int i = 0; i < 6; i++)
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
		if (Input.GetKey("m"))//stand
		{
			Move(rightKnee, 115, 1f);
			Move(rightElbow, -120, 1f);
			Move(rightHip, -100, 1f);
			Move(rightAnkle, 0, 1f);
			Move(rightShoulder, 55, 1f);
		}
		if (Input.GetKey("n"))//crouch
		{
			Move(rightElbow, -170, 1f);
			Move(rightHip, -180, 1f);
			Move(rightAnkle, -70, 1f);
			Move(rightKnee, 260, 1f);
			Move(rightShoulder, 55, 1f);
		}	
		if (Input.GetKey("z")) //alternate forward
		{
			Move(rightAnkle, -20, 1f);
			Move(rightHip, -170, 1f);
			Move(rightElbow, -210, 1f);
			Move(rightKnee, 110, 1f);
		}
		if (Input.GetKey("x")) //backwards
		{
			Move(rightKnee, 250, 1f);
			Move(rightHip, -120, 1f);
			Move(rightElbow, -120, 1f);
			Move(rightAnkle, -55, 1f);
			Move(rightShoulder, 45, 1f);
		}
		if (Input.GetKey("c")) // forward
		{
			Move(rightAnkle, -55, 1f);
			Move(rightHip, -180, 1f);
			Move(rightElbow, -200, 1f);
			Move(rightKnee, 190, 1f);
			Move(rightShoulder, 45, 1f);
		}
		if (Input.GetKey("y")) //resets
		{
			SceneManager.LoadScene("SampleScene");
		}
		for (int i = 0; i < 6; i++)
		/// This will lock any joint that is within 1 degree of its limit angle
		{
			if (allAngles[i] < allJoints[i].angle + 95f && allAngles[i] > allJoints[i].angle + 85f)
			{
				Lock(allJoints[i]);
			}
		}

	}
}

