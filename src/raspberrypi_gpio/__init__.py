from .IGpioClient import IGpioClient
try: # try block so we can run the mock on windows
    from .GPioClient import GpioClient
except ModuleNotFoundError as e:
    pass
