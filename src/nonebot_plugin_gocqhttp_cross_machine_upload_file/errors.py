class UnsupportedDriverError(RuntimeError):
    def __init__(self):
        super().__init__("Only FastAPI Driver is supported")
