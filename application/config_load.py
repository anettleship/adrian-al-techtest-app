import os
from dotenv import load_dotenv
from . config_stages import stage_list

# don't use enum, just add each class to a dictionary and lookup from the environment variable

load_dotenv()

stage_name = os.environ.get("STAGE")

application_config = stage_list[stage_name]()