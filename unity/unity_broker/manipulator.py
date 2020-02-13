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
        self.unity_reference.close_gripper()

    def open_gripper(self,):
        """
        Open gripper of ROV's robotic arm
        """
        self.unity_reference.open_gripper()
