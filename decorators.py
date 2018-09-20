import functools
import time

RETRY_LIMIT = 5
RETRY_DELAY = 0.2

def retry(function):
    """
    A decorator that wraps the passed in function and re-executes it
    until the RETRY_LIMIT with a RETRY_DELAY between executions.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        for i in range(RETRY_LIMIT):
            try:
                if i != 0:
                    print("Trying again...")
                return function(*args, **kwargs)
            except Exception as e:
                # log the exception
                err = "There was an exception in  "
                err += function.__name__
                print(err)
                print(e)
                time.sleep(RETRY_DELAY)
        print("Failed executing %s. Skipping video..." %function.__name__)
        return False
    return wrapper

def exception(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
 
    @param logger: The logging object
    """
 
    def decorator(func):
 
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
                # re-raise the exception
                raise

        return wrapper
    return decorator