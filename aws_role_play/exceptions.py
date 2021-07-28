def handle_exception(exception, is_debug=False):
    if is_debug:
        raise exception
    print(f"{type(exception).__name__} {exception}")
