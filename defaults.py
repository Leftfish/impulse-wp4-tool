class ResultsDict(dict):
    """
    A dictionary subclass to hold results with predefined keys.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault('green', [])
        self.setdefault('yellow', [])
        self.setdefault('red', [])
        self.setdefault('info', [])
        self.setdefault('rights_green', [])
        self.setdefault('rights_yellow', [])
