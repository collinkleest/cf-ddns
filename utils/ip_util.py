import requests

class IPUtility:
    @staticmethod
    def get_public_ip():
        try:
            response = requests.get('https://api64.ipify.org?format=json')
            if response.status_code == 200:
                ip_data = response.json()
                return ip_data.get('ip')
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None