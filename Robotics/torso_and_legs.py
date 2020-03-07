from positions_sym import positions

crunched_pos = positions['crunched']
extended_pos = positions['extended']

torso_list = {'RHP', 'LHP', 'RSP', 'LSP', 'RSR', 'LSR', 'RER', 'LER', 'REY', 'LEY', 'RWY', 'LWY'}
hips = extended_pos['RHP'] - crunched_pos['RHP']

torso_dict = {}
for joint in torso_list:
    value = (extended_pos[joint] - crunched_pos[joint])/hips
    torso_dict[joint] = value

torso_speed = {}
max_angles_torso = max(torso_dict.values())
for joint in torso_list:
    speed = torso_dict[joint]/max_angles_torso
    torso_speed[joint] = speed

legs = ['RKP', 'LKP', 'LAP', 'RAP']
knees = extended_pos['RKP'] - crunched_pos['RKP']

legs_dict = {}
for joint in legs:
    value = (extended_pos[joint] - crunched_pos[joint])/knees
    legs_dict[joint] = value

legs_speed = {}
max_angles_legs = max(legs_dict.values())
for joint in legs_dict:
    speed = legs_dict[joint]/max_angles_legs
    legs_speed[joint] = speed
