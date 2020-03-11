from Robot_position_test import set_posture

#prompt = '> '
posture_now = 'extended'
while True:
    x = raw_input("Switch Position?")
    if x == '':
        if posture_now == "extended":
            set_posture("crunched")
            posture_now = "crunched"
        elif posture_now == "crunched":
            set_posture("extended")
            posture_now = "extended"
    if x != '':
        print "ERROR ERROR ERROR ERROR"
