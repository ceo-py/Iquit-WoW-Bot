class ValidationTreeCommands:
    @staticmethod
    def hour(value):
        return not 0 <= value <= 24

    @staticmethod
    def minute(value):
        return not 0 <= value <= 59
