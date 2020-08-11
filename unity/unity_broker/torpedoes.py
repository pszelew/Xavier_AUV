from pytransdec import Actions

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
        return self.unity_reference.observations['torpedo_ready']

    def fire(self):
        """
        Launch single torpedo
        """
        self.unity_reference.set_vector_action(Actions.TORPEDO, 1)
