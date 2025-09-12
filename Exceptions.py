class SensorException(Exception):
    def __init__(self, message,error_code):
        super().__init__(message)
        self.error_code = error_code


    def __str__(self):
        return f'{self.args[0]}(Error raised with code: {self.error_code})'


    def validate (self, sensor):
        pass


class PDFException(Exception):
    def __init__(self, message,error):
        super().__init__(message)
        self.error = error

    def __str__(self):
        return f"{self.args[0]}(Error raised with code: {self.error})"

class RepositoryException(Exception):
    def __init__(self, message,error):
        super().__init__(message)
        self.error = error

    def __str__(self):
        return f"{self.args[0]}(Error raised with code: {self.error})"
