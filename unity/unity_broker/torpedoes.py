class Torpedoes:
    """
    Control ROV's torpedo launcher
    """
    def __init__(self, unity_reference):
        self.unity_reference = unity_reference

    def is_torpedo_ready(self):
        """
        Check if torpedo is ready to lunch
        :return: True when torpedo is ready to lunch
        """
        return True

    def fire(self):
        """
        Lunch single torpedo
        """
        self.unity_reference.torpedo_fire()
