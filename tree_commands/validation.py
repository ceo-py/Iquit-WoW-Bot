class ValidationTreeCommands:

    @staticmethod
    def hour(value):
        return not 0 <= value <= 24

    @staticmethod
    def minutes(value):
        return not 0 <= value <= 60


