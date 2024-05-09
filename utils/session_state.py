class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def reset(self):
        self.__dict__.clear()
