using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Move : MonoBehaviour
{   
    //Do i need to put all body parts in grrrr? Seperate code for left and right?
    //Create joint variables
    HingeJoint Elbow;
    HingeJoint Shoulder;
    HingeJoint Ankle;
    HingeJoint Knee;
    HingeJoint Hip;
    HingeJoint Neck;

    //Joint limits
    JointAngleLimits ElbowLim;
    JointAngleLimits ShoulderLim;
    JointAngleLimits AnkleLim;
    JointAngleLimits KneeLim;
    JointAngleLimits HipLim;
    JointAngleLimits NeckLim;

    //Joint motors
    JointMotor ElbowMotor;
    JointMotor ShoulderMotor;
    JointMotor AnkleMotor;
    JointMotor KneeMotor;
    JointMotor HipMotor;
    JointMotor NeckMotor;

    
    // Start is called before the first frame update
    void Start()
    //Find joints
    {
        Elbow = GameObject.Find("LeftForearm").GetComponent<Rigid
        Shoulder = 
        Ankle = 
        Knee = 
        Hip = 
        Neck = 
    }

    
    // Update is called once per frame
    void Update()
    {
        
    }
}
