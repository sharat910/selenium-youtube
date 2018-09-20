import logging 

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("youtube_player")
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler("/path/to/test.log")
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger