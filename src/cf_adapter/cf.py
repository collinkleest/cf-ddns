from logging import Logger
from typing import List

import requests
from requests import Response
from utils.timestamp import TimestampService
import json


class CfAdapter:

    def __init__(
        self,
        api_key: str,
        cf_email: str,
        ip_address: str,
        logger: Logger,
        cf_domain="https://api.cloudflare.com",
        cf_api_version="v4",
        black_listed_domains={},
    ) -> None:
        self.api_key = api_key
        self.cf_email = cf_email
        self.ip_address = ip_address
        self.logger = logger
        self.cf_domain = cf_domain
        self.cf_api_version = cf_api_version
        self.headers = self.construct_headers()
        self.black_listed_domains = black_listed_domains
        self.timestamp_service = TimestampService()

    def get_zone_ids(self) -> List[str]:
        zone_ids: List[str] = []
        try:
            response = requests.get(
                f"{self.cf_domain}/client/{self.cf_api_version}/zones",
                headers=self.headers,
            )

            if response.status_code == 200:
                json_data = response.json()
                for result in json_data["result"]:
                    zone_ids.append(result["id"])
                return zone_ids
            else:
                self.logger.error(
                    f"Error when getting zone ids: {response.text}")
                return zone_ids
        except Exception as e:
            self.logger.error(f"Exception found when getting zone ids: {e}")
            return zone_ids

    def construct_headers(self) -> dict:
        return {"X-Auth-Email": self.cf_email, "X-Auth-Key": self.api_key}

    def is_another_page_available(self, result_info: dict) -> bool:
        return result_info["page"] != result_info["total_pages"]

    def fetch_dns_records(self, zone_id, page_number=1) -> Response:
        return requests.get(
            f"{self.cf_domain}/client/{self.cf_api_version}/zones/{zone_id}/dns_records?page={page_number}",
            headers=self.headers,
        )

    def fetch_domains(self, zone_id: str) -> List[dict]:
        domains: List[dict] = []
        try:
            response = self.fetch_dns_records(zone_id)

            json_data = response.json()
            result_info = json_data["result_info"]

            domains = json_data["result"]

            if response.status_code == 200:
                while self.is_another_page_available(result_info):
                    response = self.fetch_dns_records(
                        zone_id, result_info["page"] + 1)
                    if response.status_code == 200:
                        json_data = response.json()
                        result_info = json_data["result_info"]
                        domains = [*domains, json_data["result"]]
                    else:
                        self.logger.error(f"Error: {response.status_code}")
                        return domains
                else:
                    return domains
            else:
                self.logger.error(f"Error: {response.status_code}")
                return domains

        except Exception as e:
            self.logger.exception(
                f"Exception found when fetching domains: {e}")
            return domains

    def construct_upload_payload(self, domain: dict, is_proxied=False) -> dict:
        return {
            "comment": f"dns record updated dynamically by cf-dns script {self.timestamp_service.get_formatted_timestamp()}",
            "content": self.ip_address,
            "name": domain["name"],
            "type": domain["type"],
            "proxied": is_proxied,
        }

    def update_domain(self, domain: dict) -> bool:
        try:
            zone_id = domain["zone_id"]
            record_id = domain["id"]
            is_proxied = domain["proxied"]
            response = requests.patch(
                f"{self.cf_domain}/client/{self.cf_api_version}/zones/{zone_id}/dns_records/{record_id}",
                data=json.dumps(
                    self.construct_upload_payload(domain, is_proxied)),
                headers=self.headers,
            )
            return response.status_code == 200 and response.json()["success"]
        except Exception as e:
            print(f"Exception found when updating domains: {e}")
            return False

    def filter_domains(self, domains: List[dict]) -> List[dict]:
        return [domain for domain in domains if self.should_update_domain(domain)]

    def should_update_domain(self, domain: dict) -> bool:
        return (
            self.is_domain_a_record(domain)
            and self.has_ip_changed(domain)
            and not self.is_domain_blacklisted(domain)
        )

    def is_domain_a_record(self, domain: dict) -> bool:
        return domain["type"] == "A"

    def has_ip_changed(self, domain: dict) -> bool:
        return domain["content"] != self.ip_address

    def is_domain_blacklisted(self, domain: dict) -> bool:
        return domain["name"] in self.black_listed_domains
