import logging
import os

os.makedirs("logs", exist_ok=True) # check folder if exist

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/app.log",
    filemode="a"
)

logger = logging.getLogger("complaints_app")
