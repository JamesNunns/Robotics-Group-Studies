from positions_sym import positions

crunched_pos = positions['crunched']
extended_pos = positions['extended']
torso_list = {'RHP', 'LHP', 'RSP', 'LSP', 'RSR', 'LSR', 'RER', 'LER', 'REY', 'LEY', 'RWY', 'LWY'}
hips = extended_pos['RHP'] - crunched_pos['RHP']
torso_dict = {}
for joint in torso_list:
    value = (extended_pos[joint] - crunched_pos[joint])/hips
    torso_dict[joint] = value

legs = ['RKP', 'LKP']
