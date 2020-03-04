﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Linq;
using System.Threading;

public class EffortParameter : MonoBehaviour
{
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

    HingeJoint leftShoulder;

    HingeJoint leftElbow;

    HingeJoint leftKnee;

    HingeJoint leftAnkle;

    HingeJoint leftHip;

    HingeJoint rightShoulder;

    HingeJoint rightElbow;

    HingeJoint rightKnee;

    HingeJoint rightAnkle;

    HingeJoint rightHip;

    HingeJoint Neck;

    List<HingeJoint> allJoints = new List<HingeJoint>();
    List<double> Torque = new List<double>();

    // Start is called before the first frame update
    void Start()
    {
        leftShoulder = GameObject.Find("LeftBicep").GetComponent<HingeJoint>();

        leftElbow = GameObject.Find("LeftForearm").GetComponent<HingeJoint>();

        leftKnee = GameObject.Find("LeftShin").GetComponent<HingeJoint>();

        leftAnkle = GameObject.Find("LeftFoot").GetComponent<HingeJoint>();

        leftHip = GameObject.Find("LeftThigh").GetComponent<HingeJoint>();

        rightShoulder = GameObject.Find("RightBicep").GetComponent<HingeJoint>();

        rightElbow = GameObject.Find("RightForearm").GetComponent<HingeJoint>();

        rightKnee = GameObject.Find("RightShin").GetComponent<HingeJoint>();

        rightAnkle = GameObject.Find("RightFoot").GetComponent<HingeJoint>();

        rightHip = GameObject.Find("RightThigh").GetComponent<HingeJoint>();

        Neck = GameObject.Find("Body").GetComponent<HingeJoint>();

        allJoints.Add(rightShoulder);
        allJoints.Add(rightElbow);
        allJoints.Add(leftShoulder);
        allJoints.Add(leftElbow);
        allJoints.Add(Neck);

        allJoints.Add(rightKnee);
        allJoints.Add(rightAnkle);
        allJoints.Add(rightHip);
        allJoints.Add(leftKnee);
        allJoints.Add(leftAnkle);
        allJoints.Add(leftHip);

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
        

    }
    double TorqueMotion(HingeJoint joint)
    /// Defining the torque created when the switching position "crunched --> extended"
    {
        /// Torque is given as (x, y, z) coordinates so to find the total torque, use pythagoras 

        return(Math.Sqrt((joint.currentTorque[0] * joint.currentTorque[0]) + (joint.currentTorque[1] * joint.currentTorque[1]) + (joint.currentTorque[2] * joint.currentTorque[2])));

    }
    // Update is called once per frame
    void Update()
    {
        /// Setting the torque for the hip, knee and ankle joints
        ///for (int i = 6; i < 12; i++)
        ///{
        ///    if (allJoints[i].velocity <= 0.5)
        ///    {
        ///        Torque[i] = 68;
        ///   }
         ///   else Torque[i] = Math.Abs(TorqueMotion(allJoints[i]));
        ///}
        ///Setting the torque for the shoulders, elbows and head joints
        ///
        for (int i=0; i < 11; i++)
        {
            if (i < 6)
            {
                if (allJoints[i].velocity <= 0.5)
                {
                    Torque[i] = 14.3;
                }
                else Torque[i] = Math.Abs(TorqueMotion(allJoints[i]));
            }
            if (i >= 6)
            {
                if (allJoints[i].velocity <= 0.5)
                {
                    Torque[i] = 68;
                }
                else Torque[i] = Math.Abs(TorqueMotion(allJoints[i]));
            }
        }

        
        print(Torque.Sum());
        
        
        

        


    }
}
