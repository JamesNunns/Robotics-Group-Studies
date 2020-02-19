using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CustomRotation : MonoBehaviour
{
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
	
	List<HingeJoint> Shoulders = new List<HingeJoint>();
	List<HingeJoint> Elbows = new List<HingeJoint>();
	List<HingeJoint> Knees = new List<HingeJoint>();
	List<HingeJoint> Ankles = new List<HingeJoint>();
	List<HingeJoint> Hips = new List<HingeJoint>();
	List<HingeJoint> allJoints = new List<HingeJoint>();
	List<float> allAngles = new List<float>();

	void Start()
	{
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
		allAngles.Add(rightElbowAngle);
		allAngles.Add(leftAnkleAngle);
		allAngles.Add(rightAnkleAngle);
		allAngles.Add(leftHipAngle);
		allAngles.Add(rightHipAngle);
		allAngles.Add(neckAngle);

	}

	void Move(HingeJoint joint, float ang, float speed)
	{   
		float direction = 1;
		if (Shoulders.Contains(joint))
		{
			ang += 90;
		}
		if (Elbows.Contains(joint))
		{
			ang = 90 - ang;
		}
		if (Hips.Contains(joint))
		{
			ang = 90 - ang;
		}
		if (joint == Neck)
		{
			ang *= -1;
			ang += 90;
		}
		for (int i = 0; i < 11; i++)
		{
			if (joint == allJoints[i])
			{
				allAngles[i] = ang;
			}
		}	
		joint.useLimits = false;
		JointMotor motor = joint.motor;
		
		if (ang < joint.angle + 90)
			{
				direction = -1;
			}
		
		motor.targetVelocity = speed*direction;
		joint.motor = motor;
		joint.useMotor = true;

	}

	void MoveSymmetric(List<HingeJoint> joints, float ang, float speed)
	{
		Move(joints[0], ang, speed);
		Move(joints[1], ang, speed);
	}

	void Lock(HingeJoint joint)
	{
		JointMotor motor = joint.motor;
		motor.targetVelocity = 0;
		joint.motor = motor;
		joint.useMotor = true;

		int ind = allJoints.IndexOf(joint);
		JointLimits limits = joint.limits;
		limits.min = allAngles[ind] -91;
		limits.max = allAngles[ind] -89;
		joint.limits = limits;
		joint.useLimits = true;
	}

	void Update()
	{
		if (Input.GetKey("m"))
		{
			MoveSymmetric(Hips, -50, 100);
		}
		if (Input.GetKey("n"))
		{
			MoveSymmetric(Knees, 70, 100);
		}	
		if (Input.GetKey("p"))
		{
			MoveSymmetric(Hips, -50, 100);
		}
		for (int i = 0; i < 11; i++)
		{
			if (allAngles[i] < allJoints[i].angle + 91 && allAngles[i] > allJoints[i].angle + 89)
			{
				Lock(allJoints[i]);
			}
		}
		print((allAngles[8], allJoints[8].angle + 90));

	}
}

