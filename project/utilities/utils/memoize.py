def memoize_instance(method):
    '''Decorator to memoize an instance method for the life time of the instance.
    Differs from memoize_forever in that the cache is stored in the object, and
    is cleaned up upon object destruction.
    '''
    cache_name = '_%s_cache' % method.__name__
    # Define wrapper function.
    def _invalidate(self):
        self.__dict__[cache_name] = {}

    # Define wrapper function.
    def _memoize_instance(self, *args, **kw):
        ''' Wrap a method so that its return values will be cached.
        Any subsequent call to the method with similar arguments will just have
        the cached result returned.
        '''
        cache = self.__dict__.setdefault(cache_name, {})
        # Try to fetch an existing result from the cache
        # frozenset is used to ensure hashability
        key = frozenset(args + tuple(kw.items()))
        try:
            return cache[key]
        except KeyError:
            # Run the function to get a result.
            result = method(self, *args, **kw)
            # Save the result in the cache.
            cache[key] = result
            return result
    # Set the invalidate function on the wrapping decorator.
    _memoize_instance.invalidate_cache = _invalidate
    return _memoize_instance