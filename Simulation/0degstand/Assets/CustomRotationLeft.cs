using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Linq;
using System;
using System.IO;

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

	HingeJoint rod;

    HingeJoint rightShoulder;
    HingeJoint rightElbow;
    HingeJoint rightKnee;
    HingeJoint rightAnkle;
    HingeJoint rightHip;

    HingeJoint Neck;

	/// Have a limiting angle for each joint
	float leftShoulderAngle;

	float leftElbowAngle;

	float leftKneeAngle;

	float leftAnkleAngle;

	float leftHipAngle;

	double Torque0 = 0;
    double Torque1 = 0;
    double Torque2 = 0;
    double Torque3 = 0;
    double Torque4 = 0;
    double Torque5 = 0;
    double Torque6 = 0;
    double Torque7 = 0;
    double Torque8 = 0;
    double Torque9 = 0;
    double Torque10 = 0;
	
	/// List every joint and angle together
	List<HingeJoint> allJoints = new List<HingeJoint>();
	List<float> allAngles = new List<float>();
	List<double> Torque = new List<double>();
	List<HingeJoint> jointsForTorque = new List<HingeJoint>();

	Dictionary<HingeJoint, float> low_cm = new Dictionary<HingeJoint, float>();
	Dictionary<HingeJoint, float> high_cm = new Dictionary<HingeJoint, float>();

	bool upperMoving;
	bool lowerMoving;

	public float TimeScale;

	void Start()
	{
		System.IO.File.WriteAllText (@"C:\users\james\Robotics-Group-Studies\Simulation\SwingAmplitude.txt", "0 ");
		/// Assign all of the defined joints to the correct game objects
		leftShoulder = GameObject.Find("LeftBicep").GetComponent<HingeJoint>();

		leftElbow = GameObject.Find("LeftForearm").GetComponent<HingeJoint>();

		leftKnee = GameObject.Find("LeftShin").GetComponent<HingeJoint>();

		leftAnkle = GameObject.Find("LeftFoot").GetComponent<HingeJoint>();

		leftHip = GameObject.Find("LeftThigh").GetComponent<HingeJoint>();
		Neck = GameObject.Find("Body").GetComponent<HingeJoint>();
		rightShoulder = GameObject.Find("RightBicep").GetComponent<HingeJoint>();
        rightElbow = GameObject.Find("RightForearm").GetComponent<HingeJoint>();
        rightKnee = GameObject.Find("RightShin").GetComponent<HingeJoint>();
        rightAnkle = GameObject.Find("RightFoot").GetComponent<HingeJoint>();
        rightHip = GameObject.Find("RightThigh").GetComponent<HingeJoint>();
		rod = GameObject.Find("RodLeft1").GetComponent<HingeJoint>();


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

		jointsForTorque.Add(rightShoulder);
        jointsForTorque.Add(rightElbow);
        jointsForTorque.Add(leftShoulder);
        jointsForTorque.Add(leftElbow);
        jointsForTorque.Add(Neck);

        jointsForTorque.Add(rightKnee);
        jointsForTorque.Add(rightAnkle);
        jointsForTorque.Add(rightHip);
        jointsForTorque.Add(leftKnee);
        jointsForTorque.Add(leftAnkle);
        jointsForTorque.Add(leftHip);

        Torque.Add(Torque0);
        Torque.Add(Torque1);
        Torque.Add(Torque2);
        Torque.Add(Torque3);
        Torque.Add(Torque4);
        Torque.Add(Torque5);
        Torque.Add(Torque6);
        Torque.Add(Torque7);
        Torque.Add(Torque8);
        Torque.Add(Torque9);
        Torque.Add(Torque10);
		
		upperMoving = false;
		lowerMoving = false;
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
			upperMoving = true;
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
			lowerMoving = true;
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

	double TorqueMotion(HingeJoint joint)
    /// Defining the torque created when the switching position "crunched --> extended"
    {
        /// Torque is given as (x, y, z) coordinates so to find the total torque, use pythagoras 

        return(Math.Sqrt((joint.currentTorque[0] * joint.currentTorque[0]) + (joint.currentTorque[1] * joint.currentTorque[1]) + (joint.currentTorque[2] * joint.currentTorque[2])));

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
		if (Input.GetKey("p")) //stand
		{
			Move(leftKnee, 115, 1f);
			Move(leftElbow, -120, 1f);
			Move(leftHip, -100, 1f);
			Move(leftAnkle, 0, 1f);
			Move(leftShoulder, 55, 1f);
		}
		if (Input.GetKey("o")) //crouch
		{
			Move(leftElbow, -170, 1f);
			Move(leftHip, -180, 1f);
			Move(leftAnkle, -70, 1f);
		    Move(leftKnee, 260, 1f);
			Move(leftShoulder, 55, 1f);
		}	
		if (Input.GetKey("z")) //alternate forward
		{
			Move(leftAnkle, -20, 1f);
			Move(leftHip, -170, 1f);
			Move(leftElbow, -210, 1f);
			Move(leftKnee, 110, 1f);
		}
		if (Input.GetKey("i")) //backwards
		{
			Move(leftKnee, 250, 1f);
			Move(leftHip, -120, 1f);
			Move(leftElbow, -120, 1f);
			Move(leftAnkle, -55, 1f);
			Move(leftShoulder, 45, 1f);
		}
		if (Input.GetKey("u")) // forward
		{
			Move(leftAnkle, -55, 1f);
			Move(leftHip, -180, 1f);
			Move(leftElbow, -200, 1f);
			Move(leftKnee, 190, 1f);
			Move(leftShoulder, 45, 1f);
		}
		if (Input.GetKey("y")) //resets
		{
			SceneManager.LoadScene("SampleScene");
		}

		for (int i = 0; i < 5; i++)
		/// This will lock any joint that is within 1 degree of its limit angle
		{
			if (allAngles[i] < allJoints[i].angle + 105f && allAngles[i] > allJoints[i].angle + 75f)
			{
				Lock(allJoints[i]);
				if (allJoints[i] == leftElbow)
				{
					upperMoving = false;
				}
				if (allJoints[i] == leftKnee)
				{
					lowerMoving = false;
				}
			}
		}
		string state = rod.angle.ToString() + " " + rod.velocity.ToString() + " " + Torque.Sum().ToString() + " " + upperMoving.ToString() + " " + lowerMoving.ToString();
		System.IO.File.WriteAllText (@"C:\users\james\Robotics-Group-Studies\Machine_Learning\state.txt", state);
		Time.timeScale = TimeScale;
		string anglevalue = rod.angle.ToString() + " ";
		File.AppendAllText(@"C:\Users\james\Robotics-Group-Studies\Simulation\SwingAmplitude.txt", anglevalue);
		
	}
}

