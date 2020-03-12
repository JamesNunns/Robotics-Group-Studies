"""
Dictionary containing the shorthand we use for each part, the short naoqi uses, and the long name some functions require
Dictionary to access the part names and sensor values for NAO including ranges of motion.


'ID' = part name, path name for parts and sensors
"""
values = {
    'AX': ['AngleX', 'Device/SubDeviceList/InertialSensor/AngleX/Sensor/Value'],
    'AY': ['AngleY', 'Device/SubDeviceList/InertialSensor/AngleY/Sensor/Value'],
    'AZ': ['AngleZ', 'Device/SubDeviceList/InertialSensor/AngleZ/Sensor/Value'],
    'GX': ["GyroscopeX", "Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value"],
    'GY': ["GyroscopeY", "Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value"],
    'GZ': ["GyroscopeZ", "Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value"],
    'ACX': ["AccelerometerX", "Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value"],
    'ACY': ["AccelerometerY", "Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value"],
    'ACZ': ["AccelerometerZ", "Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value"],
    'BC': ["Battery", "Device/SubDeviceList/Battery/Charge/Sensor/Value"],
    'HY': ["HeadYaw", "Device/SubDeviceList/HeadYaw/Position/Sensor/Value"],
    'HP': ["HeadPitch", "Device/SubDeviceList/HeadPitch/Position/Sensor/Value"],
    'RSR': ["RShoulderRoll", "Device/SubDeviceList/RShoulderRoll/Position/Sensor/Value"],
    'RSP': ["RShoulderPitch", "Device/SubDeviceList/RShoulderPitch/Position/Sensor/Value"],
    'RER': ["RElbowRoll", "Device/SubDeviceList/RElbowRoll/Position/Sensor/Value"],
    'REY': ["RElbowYaw", "Device/SubDeviceList/RElbowYaw/Position/Sensor/Value"],
    'RWY': ["RWristYaw", "Device/SubDeviceList/RWristYaw/Position/Sensor/Value"],
    'RH': ["RHand", "Device/SubDeviceList/RHand/Position/Sensor/Value"],
    'RHP': ["RHipPitch", "Device/SubDeviceList/RHipPitch/Position/Sensor/Value"],
    'RKP': ["RKneePitch", "Device/SubDeviceList/RKneePitch/Position/Sensor/Value"],
    'RAP': ["RAnklePitch", "Device/SubDeviceList/RAnklePitch/Position/Sensor/Value"],
    'RAR': ["RAnkleRoll", "Device/SubDeviceList/RAnkleRoll/Position/Sensor/Value"],
    'LSR': ["LShoulderRoll", "Device/SubDeviceList/LShoulderRoll/Position/Sensor/Value"],
    'LSP': ["LShoulderPitch", "Device/SubDeviceList/LShoulderPitch/Position/Sensor/Value"],
    'LER': ["LElbowRoll", "Device/SubDeviceList/LElbowRoll/Position/Sensor/Value"],
    'LEY': ["LElbowYaw", "Device/SubDeviceList/LElbowYaw/Position/Sensor/Value"],
    'LWY': ["LWristYaw", "Device/SubDeviceList/LWristYaw/Position/Sensor/Value"],
    'LH': ["LHand", "Device/SubDeviceList/LHand/Position/Sensor/Value"],
    'LHP': ["LHipPitch", "Device/SubDeviceList/LHipPitch/Position/Sensor/Value"],
    'LKP': ["LKneePitch", "Device/SubDeviceList/LKneePitch/Position/Sensor/Value"],
    'LAP': ["LAnklePitch", "Device/SubDeviceList/LAnklePitch/Position/Sensor/Value"],
    'LAR': ["LAnkleRoll", "Device/SubDeviceList/LAnkleRoll/Position/Sensor/Value"]
}
