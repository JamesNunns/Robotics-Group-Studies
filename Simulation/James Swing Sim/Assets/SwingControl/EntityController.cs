using PythonInterface.Interfaces;
using System.Collections.Generic;
using UnityEngine;
using static PythonInterface.Interfaces.FitnessFunctions;

public class EntityController : MonoBehaviour
{

    readonly GameObject swing; //Definition of physical gameobject

    //TODO: Make motorLims and maxV dependant on the limb in question
    readonly float motorLimits = 90; //Define limits of the furthest the motors can move
    readonly float maxV = 5; //define largest angle change possible in a single step

    JointAngleLimits2D lims;

    readonly GameObject swingElements;
    readonly GameObject robotElements;

    public GenericEntity swingAI;

    readonly List<HingeJoint2D> inputObjects = new List<HingeJoint2D>();
    readonly List<HingeJoint2D> outputObjects = new List<HingeJoint2D>();

    public float reward;

    readonly FitnessFunctions.FitnessFunctionDelegate fitnessFunctionToUse;

    public int inputLength;
    public int outputLength;

    List<float> velocities = new List<float>();

    public EntityController(GameObject swingObject, GenericEntity entity, FitnessFunctionDelegate fitnessFunction)
    {
        swing = swingObject;
        swingElements = swing.transform.Find("Swing").gameObject;
        robotElements = swing.transform.Find("Robot").gameObject;
        swingAI = entity;
        fitnessFunctionToUse = fitnessFunction;
    }

    // Start is called before the first frame update
    void Start()

    // Call each of the body parts
    {
        //Adds swing hinges to the list of inputs
        Component[] rawInputs = swingElements.GetComponentsInChildren<HingeJoint2D>();
        foreach (HingeJoint2D joint in rawInputs)
        {
            inputObjects.Add(joint);
            velocities.Add(0); //initialises velocities list to be zeros of the correct length
        }

        //Adds robot hinges to the list of inputs and outputs
        rawInputs = robotElements.GetComponentsInChildren<HingeJoint2D>();
        foreach (HingeJoint2D joint in rawInputs)
        {
            inputObjects.Add(joint);
            outputObjects.Add(joint);
        }

        inputLength = inputObjects.Count + rawInputs.Length; //then tell the AI the length of the list. rawInputs length is added to account for the addition of velocity data later on
        outputLength = outputObjects.Count;
    }

    private void FixedUpdate()
    {
        reward = fitnessFunctionToUse(swing, this);
        MoveSelf();
    }

    // Define a locking function

    private void ChangeHingeAngle(HingeJoint2D hinge, float ang)
    {
        if (lims.min + ang > motorLimits)
        {
            lims.min = motorLimits;
            lims.max = motorLimits;
        }
        else if (lims.min + ang < -motorLimits)
        {
            lims.min = -motorLimits;
            lims.max = -motorLimits;
        }
        else
        {
            lims.min += ang;
            lims.max += ang;
        }
        hinge.limits = lims;
        hinge.useLimits = true;
    }

    private void MoveSelf()
    {
        List<float> inputs = new List<float>();
        foreach (HingeJoint2D hinge in inputObjects)
        {
            inputs.Add(hinge.transform.rotation.x / motorLimits);
        }
        foreach (float v in velocities)
        {
            inputs.Add(v);
        }

        List<float> movements = swingAI.DoAction(inputs, reward);
        velocities = movements;
        //TODO: Move limits logic to here, so velocities take lims into account, not just AI output
        for (int i = 0; i < movements.Count; i++)
        {
            ChangeHingeAngle(outputObjects[i], movements[i] * maxV);
        }
    }

    public float KillSelf()
    {
        Destroy(swing);
        return reward;
    }
}
