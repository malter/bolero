import inspect


class Base(object):
    """Base class for all objects in BOLeRo."""

    @classmethod
    def _get_param_names(cls):
        """Get parameter names for the estimator.

        Returns
        -------
        args : list of strings
            List of constructor parameters
        """
        # introspect the constructor arguments to find the model parameters
        # to represent
        args, varargs, kw, default = inspect.getargspec(cls.__init__)
        if varargs is not None:
            raise RuntimeError("BOLeRo objects should always specify their "
                               "parameters in the signature of their __init__ "
                               " (no varargs). %s doesn't follow this "
                               "convention." % (cls,))
        # Remove 'self'
        args.pop(0)
        args.sort()
        return args

    def get_params(self):
        """Get parameters for this estimator.

        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        return dict((key, getattr(self, key, None))
                    for key in self._get_param_names())

    def __repr__(self):
        params_dict = self.get_params()
        params = ", ".join(["%s=%s" % (name, params_dict[name])
                            for name in self._get_param_names()])
        return '%s(%s)' % (self.__class__.__name__, params)
