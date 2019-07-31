def module_permission(func):
    def wrapper(self, *args, **kwargs):
        user = self.request.user
        print("[DEBUG]: enter {}()".format(self.request.user.mobile))
        return func(self, *args, **kwargs)
    return wrapper