import logging
import colorlog

def setup_logger():
    # 1. Create a Handler (Stream to Console)
    handler = colorlog.StreamHandler()
    
    # 2. Define the "Cyberpunk" Format
    # %(asctime)s  = Timestamp
    # %(log_color)s = Changes color based on level
    # %(message)s  = The actual text
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(message)s",
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    handler.setFormatter(formatter)

    # 3. Create the Logger
    logger = logging.getLogger('Pythia')
    logger.addHandler(handler)
    
    # 4. Set Level (INFO = Show everything except debug noise)
    logger.setLevel(logging.INFO)
    
    return logger

# Create the singleton instance
logger = setup_logger()