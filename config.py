import json
import sys
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
import time

CONFIG_FILE = Path("config.json")

class SiteConfig(BaseModel):
    # Site Meta
    site_name: str = "Portfolio"
    site_description: str = "A personal portfolio built with FastAPI and SQLite."
    author_name: str = "System Administrator"
    copyright_year: int = 2024
    
    # URLs
    github_url: str = "https://github.com/yourusername"
    linkedin_url: Optional[str] = ""
    
    # Legal / Impressum
    legal_name: str = "Max Mustermann"
    legal_address: str = "Musterstraße 1, 12345 Musterstadt, Germany"
    legal_email: str = "contact [at] domain [dot] com"
    legal_phone: str = "+49 123 456789"
    
    # Admin Auth
    admin_user: str = "changeadmin"  # Default to be changed
    admin_pass: str = "changepass"  # Default to be changed

def load_config() -> SiteConfig:
    """Loads config from file or creates default if missing."""
    if not CONFIG_FILE.exists():
        print(f"[!] Config file not found. Creating default: {CONFIG_FILE}")
        default_config = SiteConfig()
        default_config.copyright_year = time.localtime().tm_year  # Set current year
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(default_config.model_dump_json(indent=4))
        print(f"[!] Please edit {CONFIG_FILE} and restart the server.")
        sys.exit(0) # Exit so user is forced to edit it

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            config = SiteConfig(**data)
            
            # check if all keys are present, if not fill in defaults
            key_was_missing = False
            for field in SiteConfig.model_fields:
                if field not in data:
                    print(f"[!] Key '{field}' was missing in config. Added default value.")
                    key_was_missing = True
                    
            if key_was_missing:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    f.write(config.model_dump_json(indent=4))
                print(f"[!] Updated {CONFIG_FILE} with missing keys. Please review and restart if needed.")
                sys.exit(0) # Exit so user can review changes
            
            # Security Check
            
            if config.admin_user == "changeadmin":
                print("\n[SECURITY ALERT] You are using the default username 'changeadmin'.")
                print(f"Please change 'admin_user' in {CONFIG_FILE} immediately.\n")
                sys.exit(1) # Refuse to start
            
            if config.admin_pass == "changepass":
                print("\n[SECURITY ALERT] You are using the default password 'changepass'.")
                print(f"Please change 'admin_pass' in {CONFIG_FILE} immediately.\n")
                sys.exit(1) # Refuse to start
                
            return config
            
    except json.JSONDecodeError:
        print(f"[ERROR] Could not parse {CONFIG_FILE}. Please check syntax.")
        sys.exit(1)

