using UnityEngine;

public class hip : MonoBehaviour
{
    public float speed;

    private Rigidbody2D rb2d;

    private HingeJoint2D hinge;

    void Start()
    {
        rb2d = GetComponent<Rigidbody2D>();
        hinge = GetComponent<HingeJoint2D>();
    }

    void FixedUpdate()
    {
        float moveHorizontal = Input.GetAxis("Horizontal");
        if (Input.GetKey("q"))
        {
            rb2d.AddTorque(-500);
        }
        if (Input.GetKey("e"))
        {
            rb2d.AddTorque(500);
        }
        hinge.useLimits = true;
    }
}
