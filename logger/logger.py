import logging

# Configure logging
logging.basicConfig(filename='../app.log', filemode='w',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
ROOT = logging.getLogger()

def get_logger():
    return ROOT

# get_logger()
# if __name__ == "__main__":
#     logger = get_logger()
#     logger.info("Hello, World!")
