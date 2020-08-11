from pytransdec import Actions

class Manipulator:
    """
    Broker for manipulator
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def close_gripper(self):
        """
        Open gripper of ROV's robotic arm
        """
        self.unity_reference.set_vector_action(Actions.GRABBER, 1)

    def open_gripper(self):
        """
        Open gripper of ROV's robotic arm
        """
        self.unity_reference.set_vector_action(Actions.GRABBER, 0)
