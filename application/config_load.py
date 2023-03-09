import os
from dotenv import load_dotenv
from . config_stages import stage_list

load_dotenv()

stage_name = os.environ.get("STAGE")

application_config = stage_list[stage_name]()