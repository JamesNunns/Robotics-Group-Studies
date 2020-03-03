using System;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// TimeScaling controlls all the time accelleration.
/// </summary>
public class TimeScaling : MonoBehaviour
{
    public float TScale;
    public Slider TimeSlider;
    private float fixedDeltaTime;
    // Start is called before the first frame update

    /// <summary>
    /// Start() selects the function to use to control the time, and sets the standard "real time"
    /// </summary>
    void Start()
    {
        TimeSlider.onValueChanged.AddListener(delegate { ChangeTScale(); });
        this.fixedDeltaTime = Time.fixedDeltaTime;
    }

    // TODO: Ensure warping timescale is stable, check other Monobehaviours for FixedUpdate
    /// <summary>
    /// ChangeTScale() gets the value of the time slider, and sets the deltatime to "Real time" * timeSlider.value
    /// </summary>
    void ChangeTScale()
    {
        TScale = TimeSlider.value;
        Time.timeScale = Convert.ToSingle(TScale);
        Time.fixedDeltaTime = this.fixedDeltaTime * Time.timeScale;
    }
}
