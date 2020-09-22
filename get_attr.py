def get_att(obj):
    for a in dir(obj):
        method = getattr(obj, a)
        if callable(method):
            try:
                print(method())
            except TypeError as e:
                print(e)
        else:
            print(method)
