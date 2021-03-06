def Singleton(cls):
    _instance = {}

    # @wraps(cls)
    def _singlenton(*args, **kargs):
        print(_instance)
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singlenton