using Interfaces;
using System.Collections.Generic;
using UnityEngine;
using static Interfaces.FitnessFunctions;

/// <summary>
/// EntityController controlls a specific swinger, and handles the world inputs feeding the AI, and back to world actions
/// </summary>
public class EntityController : MonoBehaviour
{

    GameObject swing; //Definition of physical gameobject

    //TODO: Make motorLims and maxV dependant on the limb in question
    readonly float motorLimits = 90; //Define limits of the furthest the motors can move
    readonly float maxV = 5; //define largest angle change possible in a single step

    JointAngleLimits2D lims;

    GameObject swingElements;
    GameObject robotElements;

    public IEntity swingAI;

    readonly List<HingeJoint2D> inputObjects = new List<HingeJoint2D>();
    readonly List<HingeJoint2D> outputObjects = new List<HingeJoint2D>();

    public float reward;

    FitnessFunctionDelegate fitnessFunctionToUse;

    public int inputLength;
    public int outputLength;

    public float Effort = 0;
    List<float> Angles { get; set; }
    List<float> Actions { get; set; }
    List<float> velocities = new List<float>();

    public void GetIOLengths(GameObject swingObject)
    {
        inputLength = swingObject.transform.Find("Swing").gameObject.GetComponentsInChildren<HingeJoint2D>().Length * 2;
        outputLength = swingObject.transform.Find("Robot").gameObject.GetComponentsInChildren<HingeJoint2D>().Length;
    }

    /// <summary>
    /// Constructor for class
    /// </summary>
    /// <param name="swingObject">Specific swing GameObject the class is attached to</param>
    /// <param name="entity">Specific instance of an IEntity which serves as the swinger's brain</param>
    /// <param name="fitnessFunction">Fitness Function to use when evaluating current state</param>
    public void Construct(GameObject swingObject, IEntity entity, FitnessFunctionDelegate fitnessFunction)
    {
        swing = swingObject;
        swingElements = swing.transform.Find("Swing").gameObject;
        robotElements = swing.transform.Find("Robot").gameObject;
        swingAI = entity;
        fitnessFunctionToUse = fitnessFunction;
    }

    // Start is called before the first frame update
    /// <summary>
    /// Start() establishes the input hinges, output hinges, and input & output lengths
    /// </summary>
    void Start()
    {
        //Adds swing hinges to the list of inputs
        if (swingElements != null)
        {
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
                outputObjects.Add(joint);
            }

            inputLength = inputObjects.Count * 2; //then tell the AI the length of the list. rawInputs length is added to account for the addition of velocity data later on
            outputLength = outputObjects.Count;
        }
    }

    /// <summary>
    /// Calculate state reward, and then perform an action
    /// </summary>
    private void FixedUpdate()
    {
        if (swing != null)
        {
            reward = fitnessFunctionToUse(Angles, velocities, Actions, this);
            MoveSelf();
        }
    }

    /// <summary>
    /// Define a function to move a hinge by a given angle
    /// </summary>
    /// <param name="hinge">HingeJoint2D object to move</param>
    /// <param name="ang">angle to change position by</param>
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

    /// <summary>
    /// Function which gathers inputs, calls the IEntity for actions, and excecutes those actions.
    /// </summary>
    private void MoveSelf()
    {
        List<float> inputs = new List<float>();
        List<float> CurrAngles = new List<float>();
        velocities = new List<float>();
        foreach (HingeJoint2D hinge in inputObjects)
        {
            CurrAngles.Add(hinge.transform.rotation.x);
            inputs.Add(hinge.transform.rotation.x / motorLimits);
        }
        for (int i = 0; i < CurrAngles.Count; i++)
        {
            velocities.Add((CurrAngles[i] - Angles[i]) / motorLimits);
        }
        foreach (float v in velocities)
        {
            inputs.Add(v);
        }

        List<float> movements = swingAI.DoAction(inputs, reward);
        for (int i = 0; i < movements.Count; i++)
        {
            ChangeHingeAngle(outputObjects[i], movements[i] * maxV);
        }
        Angles = CurrAngles;
    }

    /// <summary>
    /// Destroys the GameObject self
    /// </summary>
    /// <returns>Returns the end-state reward of the swing</returns>
    public float KillSelf()
    {
        Destroy(swing);
        return reward;
    }
}
