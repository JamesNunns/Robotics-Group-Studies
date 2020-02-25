using System;
using UnityEngine;
using UnityEngine.UI;

public class TimeScaling : MonoBehaviour
{
    public float TScale;
    public Slider TimeSlider;
    private float fixedDeltaTime;
    // Start is called before the first frame update
    void Start()
    {
        TimeSlider.onValueChanged.AddListener(delegate { ChangeTScale(); });
        this.fixedDeltaTime = Time.fixedDeltaTime;
    }

    // Update is called once per frame
    // TODO: Ensure warping timescale is stable, check other Monobehaviours for FixedUpdate
    void ChangeTScale()
    {
        TScale = TimeSlider.value;
        Time.timeScale = Convert.ToSingle(TScale);
        Time.fixedDeltaTime = this.fixedDeltaTime * Time.timeScale;
    }
}
