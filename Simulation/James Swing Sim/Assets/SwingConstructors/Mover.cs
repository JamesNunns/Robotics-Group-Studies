using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Mover : MonoBehaviour
{
	// Create variables of all of the individual pieces of the body
	Rigidbody2D thigh;
 	Rigidbody2D leg;
	Rigidbody2D foot;
	Rigidbody2D torso;
	Rigidbody2D upperarm;
	Rigidbody2D forearm;
	// Joints
	HingeJoint2D knee;
	HingeJoint2D ankle;
	HingeJoint2D shoulder;
	HingeJoint2D hip;
	// Joint limits
	JointAngleLimits2D kneelims;
	JointAngleLimits2D anklelims;
	JointAngleLimits2D shoulderlims;
	JointAngleLimits2D hiplims;
	// Joint motors
	JointMotor2D kneemotor;
	JointMotor2D anklemotor;
	JointMotor2D shouldermotor;
	JointMotor2D hipmotor;

    // Start is called before the first frame update
    void Start()

    // Call each of the body parts
    {
    	thigh = GameObject.Find("Thigh").GetComponent<Rigidbody2D>();
    	leg = GameObject.Find("Leg").GetComponent<Rigidbody2D>();
        knee = GameObject.Find("Leg").GetComponent<HingeJoint2D>();
        foot = GameObject.Find("Foot").GetComponent<Rigidbody2D>();
        ankle = GameObject.Find("Foot").GetComponent<HingeJoint2D>();
        torso = GameObject.Find("Torso").GetComponent<Rigidbody2D>();
        upperarm = GameObject.Find("UpperArm").GetComponent<Rigidbody2D>();
        shoulder = GameObject.Find("UpperArm").GetComponent<HingeJoint2D>();
        forearm = GameObject.Find("Forearm").GetComponent<Rigidbody2D>();
    	hip = GameObject.Find("Torso").GetComponent<HingeJoint2D>();

    	kneelims = knee.limits;
    	anklelims = ankle.limits;
    	shoulderlims = shoulder.limits;
    	hiplims = hip.limits;

    	kneemotor = knee.motor;
    	anklemotor = ankle.motor;
    	shouldermotor = shoulder.motor;
    	hipmotor = hip.motor;
    	
    }
    // Define a locking function


    private void KneeAngle(float ang)
    // Locks the knee joint at the passed anlge
    {
    	kneelims.min = ang;
    	kneelims.max = ang;
    	knee.limits = kneelims;
    	knee.useLimits = true;

    }
    private void AnkleAngle(float ang)
    // Locks the ankle joint at the passed angle
    {
    	anklelims.min = ang;
    	anklelims.max = ang;
    	ankle.limits = anklelims;
    	ankle.useLimits = true;
    }
    private void ShoulderAngle(float ang)
    // Locks the shoulder joint at the passed angle
    {
    	shoulderlims.min = ang;
    	shoulderlims.max = ang;
    	shoulder.limits = shoulderlims;
    	shoulder.useLimits = true;
    }
    private void HipAngle(float ang)
    // Locks the hip joint at the passed angle
    {
    	hiplims.min = ang;
    	hiplims.max = ang;
    	hip.limits = hiplims;
    	hip.useLimits = true;
    }
    private void Unlocking()
    // Unlocks the joints so they can be moved manually
    {
    	// Set limits of hinges
    	JointAngleLimits2D kneelims = knee.limits;
    	kneelims.min = 20;
    	kneelims.max = 180;
    	knee.limits = kneelims;
    	knee.useLimits = true;

    	JointAngleLimits2D anklelims = ankle.limits;
    	anklelims.min = -150;
    	anklelims.max = -30;
    	ankle.limits = anklelims;
    	ankle.useLimits = true;

    	JointAngleLimits2D shoulderlims = shoulder.limits;
    	shoulderlims.min = -140;
    	shoulderlims.max = -50;
    	shoulder.limits = shoulderlims;
    	shoulder.useLimits = true;

    	JointAngleLimits2D hiplims = hip.limits;
    	hiplims.min = 50;
    	hiplims.max = 150;
    	hip.limits = hiplims;
    	hip.useLimits = true;

    }
    // Update is called once per frame
    void Update()
    {

    	if (Input.GetKey("n"))
    	{
    		Unlocking();
    	}

    	if (Input.GetKey("c"))
    	{
    		KneeAngle(160);
    	}

    	if (Input.GetKey("v"))
    	{
    		KneeAngle(30);
    	}

    	if (Input.GetKey("f"))
    	{
    		KneeAngle(130);
    	}

    	if (Input.GetKey("g"))
    	{
    		KneeAngle(100);
    	}

    	if (Input.GetKey("h"))
    	{
    		KneeAngle(70);
    	}

    	if (Input.GetKey("j"))
        {
        	KneeAngle(40);
        }
    }
}
