

from typing import List

import requests
import json

class CfAdapter:

    def __init__(self, api_key: str, cf_email: str, zone_ids: str, ip_address: str, cf_domain='https://api.cloudflare.com', cf_api_version='v4') -> None:
        self.api_key = api_key
        self.cf_email = cf_email
        self.ip_address = ip_address
        self.zone_ids = self.construct_zone_ids(zone_ids)
        self.cf_domain = cf_domain
        self.cf_api_version = cf_api_version

    def construct_zone_ids(self, zone_ids: str) -> List[str]:
        if not zone_ids:
            return []

        result_array = zone_ids.split(',')
        result_array = [element.strip() for element in result_array]
        return result_array

    def construct_headers(self) -> dict:
        return {
            'X-Auth-Email': self.cf_email,
            'X-Auth-Key': self.api_key
        }

    def fetch_domains(self, zone_id: str) -> dict:
        try:
            response = requests.get(
                f'{self.cf_domain}/client/{self.cf_api_version}/zones/{zone_id}/dns_records', headers=self.construct_headers())

            if response.status_code == 200:
                json_data = response.json()
                return json_data
            else:
                print(f"Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception found when fetching domains: {e}")
            return []

    def construct_upload_payload(self, domain: dict) -> dict:
        return {
            "content": self.ip_address,
            "name": domain['name'],
            "type": domain['type'],
            "proxied": True
        }

    def update_domain(self, domain: dict) -> bool:
        try:
            zone_id = domain['zone_id']
            record_id = domain['id']
            response = requests.put(f'{self.cf_domain}/client/{self.cf_api_version}/zones/{zone_id}/dns_records/{record_id}',
                                    data=json.dumps(self.construct_upload_payload(domain)), headers=self.construct_headers())
            return response.status_code == 200 and response.json()['success']
        except Exception as e:
            print(f"Exception found when updating domains: {e}")
            return False

    def filter_domains_by_a_record(self, domains: dict) -> List[dict]:
        domains = domains['result']
        return [domain for domain in domains if domain['type'] == "A"]

    def filter_domains_by_ip_address(self, domains: List[dict]) -> List[dict]:
        return [domain for domain in domains if domain['content'] != self.ip_address]
