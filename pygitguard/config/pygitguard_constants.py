import yaml

PYGITGUARD_FILENAME = ".pygitguard.yaml"

INTERNAL_FILE_IGNORE = [
    PYGITGUARD_FILENAME,
    "requirements.txt",
    ".gitignore",
    "pygitguard_constants.py",
]
# Patterns for sensitive filenames (regex)
SENSITIVE_PATTERNS = [
    r".*\.env(\..*)?$",  # .env, .env.local, .env.prod, my.env
    r".*\.pem(\..*)?$",  # .pem, .pem.bak, .pem.old, mykey.pem
    r".*\.key(\..*)?$",  # .key, .key.bak, .key.txt, server.key
    r".*\.crt(\..*)?$",  # .crt, .crt.pem, .crt.bak, cert.crt
    r".*\.sqlite(\..*)?$",  # .sqlite, .sqlite3, .sqlite.bak, data.sqlite
    r".*\.db(\..*)?$",  # .db, .db.bak, .db.sqlite, prod.db
    r".*secret[s]?(\..*)?$",  # secret.txt, secrets.json, mysecrets.txt
    r".*credential[s]?(\..*)?$",  # credential.json, credentials.txt, usercredentials.csv
    r".*private\.key(\..*)?$",  # private.key, private.key.bak, myprivate.key
    r".*id_rsa(\..*)?$",  # id_rsa, id_rsa.pub, backup_id_rsa
    r".*id_dsa(\..*)?$",  # id_dsa, id_dsa.pub, backup_id_dsa
    r".*credentials(\..*)?$",  # aws_credentials, aws_credentials.txt, my_aws_credentials
    r".*passwords?(\..*)?$",  # passwords.txt, my_passwords.json, blabla_password.txt
    r".*apikeys?(\..*)?$",  # apikeys.txt, blabla_apikey.txt, apikey.json
    r".*api_keys?(\..*)?$",  # api_keys.txt, blabla_api_key.txt, api_key.json
    r".*tokens?(\..*)?$",  # tokens.txt, my_token.json, blabla_token.txt
    r".*usernames?(\..*)?$",  # usernames.txt, admin_username.json, blabla_username.txt
    r".*users?(\..*)?$",  # users.txt, db_user.json, blabla_user.txt
    r".*ACCESS_KEYs?(\..*)?$",  # ACCESS_KEY.txt, my_ACCESS_KEYS.json, blabla_ACCESS_KEY.txt
]

# Patterns for sensitive content inside files (regex)
SENSITIVE_CONTENT = [
    r"\b\w*password\w*\s*=\s*['\"`].+['\"`]",  # password = '...', my_password = "...", password_my = '...'
    r"\b\w*passwords\w*\s*=\s*['\"`].+['\"`]",  # passwords = '...', my_passwords = "...", passwords_my = '...'
    r"\b\w*apikey\w*\s*=\s*['\"`].+['\"`]",  # apikey = '...', my_apikey = "...", apikey_my = '...'
    r"\b\w*apikeys\w*\s*=\s*['\"`].+['\"`]",  # apikeys = '...', my_apikeys = "...", apikeys_my = '...'
    r"\b\w*api_key\w*\s*=\s*['\"`].+['\"`]",  # api_key = '...', my_api_key = "...", api_key_my = '...'
    r"\b\w*api_keys\w*\s*=\s*['\"`].+['\"`]",  # api_keys = '...', my_api_keys = "...", api_keys_my = '...'
    r"\b\w*token\w*\s*=\s*['\"`].+['\"`]",  # token = '...', my_token = "...", token_my = '...'
    r"\b\w*tokens\w*\s*=\s*['\"`].+['\"`]",  # tokens = '...', my_tokens = "...", tokens_my = '...'
    r"\b\w*username\w*\s*=\s*['\"`].+['\"`]",  # username = '...', my_username = "...", username_my = '...'
    r"\b\w*usernames\w*\s*=\s*['\"`].+['\"`]",  # usernames = '...', my_usernames = "...", usernames_my = '...'
    r"\b\w*user\w*\s*=\s*['\"`].+['\"`]",  # user = '...', my_user = "...", user_my = '...'
    r"\b\w*users\w*\s*=\s*['\"`].+['\"`]",  # users = '...', my_users = "...", users_my = '...'
    r"\b\w*ACCESS_KEY\w*\s*=\s*['\"`].+['\"`]",  # ACCESS_KEY = '...', my_ACCESS_KEY = "...", ACCESS_KEY_my = '...'
    r"\b\w*ACCESS_KEYS\w*\s*=\s*['\"`].+['\"`]",  # ACCESS_KEYS = '...', my_ACCESS_KEYS = "...", ACCESS_KEYS_my = '...'
]

# List of best practice files to check for in the project root
BEST_PRACTICES_FILES = [
    ".gitignore",  # .gitignore file
    {"Dockerfile": ".dockerignore"},  # Dockerfile should have a .dockerignore
    {
        "docker-compose.yml": ".dockerignore"
    },  # docker-compose.yml should have a .dockerignore
    "README.md",  # Project documentation
    "LICENSE",  # License file
    "requirements.txt",  # Python dependencies
    "pyproject.toml",  # Build system and tool configuration (recommended for all Python projects)
]

# Maximum file size (in MB) to scan for sensitive content
MAX_FILE_SIZE_MB = 1  # e.g., 1 means files larger than 1MB will be skipped
