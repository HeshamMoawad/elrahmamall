from threading import Lock


class SingletonMeta(type):
    """
    A metaclass that ensures only one instance of a class is created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Check if an instance of the class already exists
        if cls not in cls._instances:
            # Create a new instance if it doesn't exist
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # Return the existing instance
        return cls._instances[cls]

class ThreadSafeSingletonMeta(type):
    """
    A thread-safe implementation of the Singleton pattern using a metaclass.
    """
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        # Double-checked locking pattern for thread safety
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
