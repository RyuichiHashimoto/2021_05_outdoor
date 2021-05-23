def imports():
    for name, val in globals().items():
        # module imports
        if isinstance(val, types.ModuleType):
            yield name, val
        # functions / callables
        if hasattr(val, '__call__'):
            yield name, val
#np.seterr(divide='ignore', invalid='ignore')
noglobal = lambda fn: types.FunctionType(fn.__code__, dict(imports()))
