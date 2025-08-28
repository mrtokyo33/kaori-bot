import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any

def load_yaml_config(path: str = 'config.yaml') -> Dict[str, Any]:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    discord_bot_token: str

    yaml_config: Dict[str, Any] = load_yaml_config()
    
    @property
    def bot_config(self) -> Dict[str, Any]:
        return self.yaml_config.get('Bot', {}) 

    @property
    def messages_config(self) -> Dict[str, Any]:
        return self.yaml_config.get('Messages', {}) 

settings = Settings()