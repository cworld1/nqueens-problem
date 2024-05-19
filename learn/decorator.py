def log(func):
    def wrapper(*args, **kw):
        print("call %s():" % func.__name__)
        return func(*args, **kw)

    return wrapper


@log
def now():
    print("2024-05-19")


if __name__ == "__main__":
    now()  # firstly call log, then continuing call now()
