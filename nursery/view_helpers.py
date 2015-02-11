def decorate_view(fn):
    """Decorate a django view class with the specified view decorator.

    For example,
        @decorate_view(login_required)
        class SomeView(View):
            pass

    Django's prescribed method of creating a MixIn class doesn't seem to work
    100% of the time, particularly with generic views.
    (https://docs.djangoproject.com/en/1.7/topics/class-based-views/intro/#decorating-the-class)
    """
    # import here to avoid nursery depending on django
    from django.utils.decorators import method_decorator

    def require(cls):
        cls.dispatch = method_decorator(fn)(cls.dispatch)
        return cls
    return require
