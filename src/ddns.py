from utils.env_manager import EnvironmentManager
from cf_adapter.cf import CfAdapter
from utils.ip_util import IPUtility
from utils.logger import Logger
from os import makedirs
from os.path import expanduser, join, exists

from dotenv import load_dotenv

load_dotenv()


CLOUDFLARE_API_KEY = EnvironmentManager.get_environment_variable(
    "CLOUDFLARE_API_KEY")
CLOUDFLARE_EMAIL = EnvironmentManager.get_environment_variable(
    "CLOUDFLARE_EMAIL")
HOME_PATH = expanduser("~")
LOG_FOLDER_NAME = 'logs'
LOG_PATH = f"{HOME_PATH}/{LOG_FOLDER_NAME}/cf-ddns.log"


def ensure_logs_directory(home_dir: str, logs_folder_name: str) -> None:
    logs_dir = join(home_dir, logs_folder_name)
    if not exists(logs_dir):
        makedirs(logs_dir)
        print(f"Created directory: {logs_dir}")
    else:
        print(f"Directory already exists: {logs_dir}")


ensure_logs_directory(HOME_PATH, LOG_FOLDER_NAME)
logger = Logger(LOG_PATH).get_logger()


def main():
    logger.info("running ddns.py, dynamic dns updater script")
    ip_utility = IPUtility()
    ip_address = ip_utility.get_public_ip(logger)
    cf_adapter = CfAdapter(
        CLOUDFLARE_API_KEY, CLOUDFLARE_EMAIL, ip_address, logger)
    zone_ids = cf_adapter.get_zone_ids()
    for zone_id in zone_ids:
        domains = cf_adapter.fetch_domains(zone_id)
        filtered_domains = cf_adapter.filter_domains(domains)
        for domain in filtered_domains:
            is_successful = cf_adapter.update_domain(domain)
            if is_successful:
                logger.info(
                    f'successfuly updated domain={domain["name"]}, type={domain["type"]}, zoneId={zone_id} to ipAddress={ip_address}'
                )
            else:
                logger.error(
                    f'failed to update domain={domain["name"]}, type={domain["type"]}, zoneId={zone_id} to ipAddress={ip_address}'
                )


if __name__ == "__main__":
    main()
