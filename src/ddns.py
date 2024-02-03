import logging
from utils.env_manager import EnvironmentManager
from cf_adapter.cf import CfAdapter
from utils.ip_util import IPUtility


CLOUDFLARE_API_KEY = EnvironmentManager.get_environment_variable("CLOUDFLARE_API_KEY")
CLOUDFLARE_EMAIL = EnvironmentManager.get_environment_variable("CLOUDFLARE_EMAIL")
CLOUDFLARE_ZONE_IDS = EnvironmentManager.get_environment_variable("CLOUDFLARE_ZONE_IDS")
LOG_PATH = './cf-ddns.log'

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print('running ddns.py, dynamic dns updater script')
    ip_utility = IPUtility()
    ip_address = ip_utility.get_public_ip()
    cf_adapter = CfAdapter(CLOUDFLARE_API_KEY, CLOUDFLARE_EMAIL, CLOUDFLARE_ZONE_IDS, ip_address)
    for zone_id in cf_adapter.zone_ids:
        domains = cf_adapter.fetch_domains(zone_id)
        filtered_domains = cf_adapter.filter_domains_by_a_record(domains)
        filtered_domains = cf_adapter.filter_domains_by_ip_address(filtered_domains)
        for domain in filtered_domains:
            is_successful = cf_adapter.update_domain(domain)
            if is_successful:
                logging.info(f'successfuly updated domain={domain["name"]}, type={domain["type"]}, zoneId={zone_id} to ipAddress={ip_address}')
            else:
                logging.error(f'failed to update domain={domain["name"]}, type={domain["type"]}, zoneId={zone_id} to ipAddress={ip_address}')

if __name__ == "__main__":
    main()