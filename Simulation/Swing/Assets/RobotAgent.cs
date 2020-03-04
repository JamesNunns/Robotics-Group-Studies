using System.Collections;
using MLAgents;
using MLAgents.Sensor;
using System.Collections.Generic;
using UnityEngine;

public class RobotAgent : Agent
{
	public CustomRotationRight right;
	public CustomRotationLeft left;
	public HingeJoint rod;
	public HingeJoint leftKnee;
	public HingeJoint rightKnee;

    // Start is called before the first frame update
    void Start()
    {
    	rod = GameObject.Find("RodLeft1").GetComponent<HingeJoint>();
    	rightKnee = GameObject.Find("RightShin").GetComponent<HingeJoint>();
    	leftKnee = GameObject.Find("LeftShin").GetComponent<HingeJoint>();
    }
    public override void AgentReset()
 	{
 		left.Move(leftKnee, Random.value*90f, 1f);
 		right.Move(rightKnee, Random.value*90f, 1f);
 	}

    public void CollectObservations(VectorSensor sensor)
	{
    // Target and Agent positions
    sensor.AddObservation(rod.angle);
    sensor.AddObservation(rod.velocity);
	}
	public override void AgentAction(float[] vectorAction)
	{
    // Actions, size = 2
    left.Move(leftKnee, vectorAction[0], vectorAction[1]);
    right.Move(leftKnee, vectorAction[0], vectorAction[1]);

    // Rewards
    float swingAngle = rod.angle;

    // Reached target
    if (swingAngle > 5)
    {
        SetReward(1.0f);
        Done();
    }

    // Fell off platform
    if (this.transform.position.y < 0)
    {
        Done();
    }
	}
  	public override float[] Heuristic()
    {
        var action = new float[2];
        action[0] = Input.GetAxis("Horizontal");
        action[1] = Input.GetAxis("Vertical");
        return action;
    
	}

}
