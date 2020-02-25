using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;

public class CustomRotation : MonoBehaviour
/// <summary>
/// This class controls the movement of the simulation
/// and attempts to replicate Nao's interface closely.
///<\summary>
{
	/// Define all the joints that can move
	HingeJoint leftShoulder;
	HingeJoint rightShoulder;

	HingeJoint leftElbow;
	HingeJoint rightElbow;

	HingeJoint leftKnee;
	HingeJoint rightKnee;

	HingeJoint leftAnkle;
	HingeJoint rightAnkle;

	HingeJoint leftHip;
	HingeJoint rightHip;

	HingeJoint Neck;

	/// Have a limiting angle for each joint
	float leftShoulderAngle;
	float rightShoulderAngle;

	float leftElbowAngle;
	float rightElbowAngle;

	float leftKneeAngle;
	float rightKneeAngle;

	float leftAnkleAngle;
	float rightAnkleAngle;

	float leftHipAngle;
	float rightHipAngle;

	float neckAngle;
	
	/// Pair up the joints for symmetrical movement
	List<HingeJoint> Shoulders = new List<HingeJoint>();
	List<HingeJoint> Elbows = new List<HingeJoint>();
	List<HingeJoint> Knees = new List<HingeJoint>();
	List<HingeJoint> Ankles = new List<HingeJoint>();
	List<HingeJoint> Hips = new List<HingeJoint>();
	/// List every joint and angle together
	List<HingeJoint> allJoints = new List<HingeJoint>();
	List<float> allAngles = new List<float>();

	void Start()
	{
		/// Assign all of the defined joints to the correct game objects
		leftShoulder = GameObject.Find("LeftBicep").GetComponent<HingeJoint>();
		rightShoulder = GameObject.Find("RightBicep").GetComponent<HingeJoint>();

		leftElbow = GameObject.Find("LeftForearm").GetComponent<HingeJoint>();
		rightElbow = GameObject.Find("RightForearm").GetComponent<HingeJoint>();

		leftKnee = GameObject.Find("LeftShin").GetComponent<HingeJoint>();
		rightKnee = GameObject.Find("RightShin").GetComponent<HingeJoint>();

		leftAnkle = GameObject.Find("LeftFoot").GetComponent<HingeJoint>();
		rightAnkle = GameObject.Find("RightFoot").GetComponent<HingeJoint>();

		leftHip = GameObject.Find("LeftThigh").GetComponent<HingeJoint>();
		rightHip = GameObject.Find("RightThigh").GetComponent<HingeJoint>();

		Neck = GameObject.Find("Body").GetComponent<HingeJoint>();

		/// Set all the starting angles to 0
		leftShoulderAngle = 0;
		rightShoulderAngle = 0;
		leftElbowAngle = 0;
		rightElbowAngle = 0;
		leftKneeAngle = 0;
		rightKneeAngle = 0;
		leftAnkleAngle = 0;
		rightAnkleAngle = 0;
		leftHipAngle = 0;
		rightHipAngle = 0;
		neckAngle = 0;

		/// Populate the lists with the correct HingeJoint objects
		Shoulders.Add(leftShoulder);
		Shoulders.Add(rightShoulder);

		Elbows.Add(leftElbow);
		Elbows.Add(rightElbow);
	
		Knees.Add(leftKnee);
		Knees.Add(rightKnee);

		Ankles.Add(leftAnkle);
		Ankles.Add(rightAnkle);

		Hips.Add(leftHip);
		Hips.Add(rightHip);
		
		allJoints.Add(leftShoulder);
		allJoints.Add(rightShoulder);
		allJoints.Add(leftElbow);
		allJoints.Add(rightElbow);
		allJoints.Add(leftKnee);
		allJoints.Add(rightKnee);
		allJoints.Add(leftAnkle);
		allJoints.Add(rightAnkle);
		allJoints.Add(leftHip);
		allJoints.Add(rightHip);
		allJoints.Add(Neck);

		allAngles.Add(leftShoulderAngle);
		allAngles.Add(rightShoulderAngle);
		allAngles.Add(leftElbowAngle);
		allAngles.Add(rightElbowAngle);
		allAngles.Add(leftKneeAngle);
		allAngles.Add(rightKneeAngle);
		allAngles.Add(leftAnkleAngle);
		allAngles.Add(rightAnkleAngle);
		allAngles.Add(leftHipAngle);
		allAngles.Add(rightHipAngle);
		allAngles.Add(neckAngle);

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
		if (Shoulders.Contains(joint))
		{
			ang += 40;
			speed *= 246;
		}
		else if (Elbows.Contains(joint))
		{
			ang *= -1;
			ang += 180;
			ang = -90 + ang;
			speed *= 246;
		}
		else if (Hips.Contains(joint))
		{
			ang = 180 + ang;
			speed *= 378;
		}
		else if (Ankles.Contains(joint))
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
		for (int i = 0; i < 11; i++)
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

	void MoveSymmetric(List<HingeJoint> joints, float ang, float speed)
	/// <summary>
	/// This method will move both joints together if they are a pair
	/// <\summary>
	{
		/// direction sets motion to be clockwise or anti
		float direction = 1;
		HingeJoint joint = joints[0];
		HingeJoint joint1 = joints[1];

		/// Some angles have to be changed because of how
		/// Nao defines its angles
		/// Also, set the speed to be in degrees per second
		if (Shoulders.Contains(joint))
		{
			ang += 40;
			speed *= 246;
		}
		else if (Elbows.Contains(joint))
		{
			ang *= -1;
			ang += 180;
			ang = -90 + ang;
			speed *= 246;
		}
		else if (Hips.Contains(joint))
		{
			ang = 180 + ang;
			speed *= 378;
		}
		else if (Ankles.Contains(joint))
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
		for (int i = 0; i < 11; i++)
		/// Set the angle in the list allAngles to the correct limit angle
		{
			if (joints.Contains(allJoints[i]))
			{
				allAngles[i] = ang;
			}
		}	
		/// Turn off joint limits temporarily
		joint.useLimits = false;
		joint1.useLimits = false;
		/// Define a motor for the joint
		JointMotor motor = joint.motor;
		JointMotor motor1 = joint1.motor;
		if (ang < joint.angle + 90)
		/// Determine direction of rotation
			{
				direction = -1;
			}
		/// Set the motor velocity, and switch the motor on
		motor.targetVelocity = speed*direction;
		motor1.targetVelocity = speed*direction;
		joint.motor = motor;
		joint1.motor = motor;
		joint.useMotor = true;
		joint1.useMotor = true;
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
		limits.min = allAngles[ind] -91;
		limits.max = allAngles[ind] -89;
		joint.limits = limits;
		joint.useLimits = true;
	}

	void Update()
	{
		/// These are test inputs, they can be changed
		if (Input.GetKey("m"))
		{
			MoveSymmetric(Knees, 90, 1f);
		}
		if (Input.GetKey("n"))
		{
			MoveSymmetric(Knees, 0, 1f);
		}	
		if (Input.GetKey("p"))
		{
			MoveSymmetric(Elbows, 20, 0.3f);
		}
		for (int i = 0; i < 11; i++)
		/// This will lock any joint that is within 1 degree of its limit angle
		{
			if (allAngles[i] < allJoints[i].angle + 95f && allAngles[i] > allJoints[i].angle + 85f)
			{
				Lock(allJoints[i]);
			}
		}

	}
}

