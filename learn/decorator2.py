def log(text):
    # get the text first
    def decorator(func):  # there it should pass param func
        def wrapper(*args, **kw):
            print("%s %s():" % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log("execute")
def now():
    print("2015-3-25")


if __name__ == "__main__":
    now()
