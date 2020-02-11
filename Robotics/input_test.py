from sys import argv


#prompt = '> '
set_posture = 'extended'
while True:
    x = raw_input("Switch Position?")
    if x == '':
        if position == "extended":
            set_posture("crunched")
            posture_now = "crunched"
        elif posture_now = "crunched":
            set_posture("extended")
            posture_now = "extended"
    if x != '':
        print "ERROR ERROR ERROR ERROR"