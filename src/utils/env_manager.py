import os
from typing import Optional

class EnvironmentManager:
    
    @staticmethod
    def get_environment_variable(key: str) -> str:
        value: Optional[str] = os.environ.get(key)

        if value is None:
            error_message = f"Environment variable {key} not found."
            print(error_message)
            raise Exception(error_message)

        return value