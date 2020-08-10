class Dropper:
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self, rpi_reference):
        self.rpi_reference = rpi_reference

    def drop_marker(self):
        pass
