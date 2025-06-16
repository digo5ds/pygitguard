<p align="center">
  <img src="docs/pygitguard.png" alt="AWS Services" width="200"/>
</p>

## 🛡️ Pygitguard

**pygitguard** is a Git project security scanner that detects:

- Exposed credentials  
- Potentially sensitive files  
- Missing best practice files  

---

## 📦 Version

**1.0.1** – First version with the basic planned functions.
  - Fix: Installer package with pip.

**1.0.0** – First version with the basic planned functions.

### Included features:

- 🚫 Detection of sensitive content using regex (e.g., passwords, tokens, API keys).
- 🧾 Identification of sensitive file patterns (e.g., `.env`, `.pem`, `id_rsa`).
- ⚠️ File size validation with configurable maximum size.
- 📄 Best practice file recommendations (e.g., `README.md`, `.gitignore`, `LICENSE`).
- ✅ Integration support with pre-commit hooks.
- ⚙️ Auto-generation of `pygitguard.yaml` and .pre-commit-config.yaml configuration file on first run.

---

It is recommended for use as a **pre-commit hook**, helping prevent critical data from being committed to version control.

---

## 🚀 How to Use
1. install:
```
pip install git+https://github.com/digo5ds/pygitguard.git
 ```
2. Configure pre-commit
- 1. Install Pre-commit (if not already installed)
```
pip install pre-commit
```
Run
```
pre-commit install
```
#If you want to run it manually, use:
1. Navigate to the root directory of your repository.  
2. Run the command:

```
pygitguard_cli
```

3. To scan a specific directory, but is recomended navigate to the root directory of your repository and run pygitguard_cli:

```
pygitguard_cli --path <your_repository>
```


---

## ⚙️ Configuration

> On first run, a configuration file named `pygitguard.yaml` will be automatically generated with default settings.




This file lets you customize pygitguard's scanning behavior. You can:

- Define sensitive file patterns (`SENSITIVE_PATTERNS`)
- Specify regex patterns to detect exposed credentials (`SENSITIVE_CONTENT`)
- List best practice files to be recommended (`BEST_PRACTICES_FILES`)
- Set a maximum allowed file size (`MAX_FILE_SIZE_MB`)
### Example `pygitguard.yaml`

```yaml
# pygitguard.yaml: Configuration file for pygitGuard.
# Edit this file to adapt the scan to your project's needs.
# RECOMMENDATION: add {project_path}/__version__.py to BEST_PRACTICES_FILES

SENSITIVE_PATTERNS:
  - .*\.env(\..*)?$
  - .*\.pem(\..*)?$
  - .*\.key(\..*)?$
  - .*\.crt(\..*)?$
  - .*\.sqlite(\..*)?$
  - .*\.db(\..*)?$
  - .*secret[s]?(\..*)?$
  - .*credential[s]?(\..*)?$
  - .*private\.key(\..*)?$
  - .*id_rsa(\..*)?$
  - .*id_dsa(\..*)?$
  - .*credentials(\..*)?$
  - .*passwords?(\..*)?$
  - .*apikeys?(\..*)?$
  - .*api_keys?(\..*)?$
  - .*tokens?(\..*)?$
  - .*usernames?(\..*)?$
  - .*users?(\..*)?$
  - .*ACCESS_KEYs?(\..*)?$

SENSITIVE_CONTENT:
  - \b\w*password\w*\s*=\s*['\`"].+['\`"]
  - \b\w*passwords\w*\s*=\s*['\`"].+['\`"]
  - \b\w*apikey\w*\s*=\s*['\`"].+['\`"]
  - \b\w*apikeys\w*\s*=\s*['\`"].+['\`"]
  - \b\w*api_key\w*\s*=\s*['\`"].+['\`"]
  - \b\w*api_keys\w*\s*=\s*['\`"].+['\`"]
  - \b\w*token\w*\s*=\s*['\`"].+['\`"]
  - \b\w*tokens\w*\s*=\s*['\`"].+['\`"]
  - \b\w*username\w*\s*=\s*['\`"].+['\`"]
  - \b\w*usernames\w*\s*=\s*['\`"].+['\`"]
  - \b\w*user\w*\s*=\s*['\`"].+['\`"]
  - \b\w*users\w*\s*=\s*['\`"].+['\`"]
  - \b\w*ACCESS_KEY\w*\s*=\s*['\`"].+['\`"]
  - \b\w*ACCESS_KEYS\w*\s*=\s*['\`"].+['\`"]

BEST_PRACTICES_FILES:
  - .gitignore
  - README.md
  - LICENSE
  - requirements.txt
  - pyproject.toml
  - Dockerfile: .dockerignore
  - docker-compose.yml: .dockerignore
  - __version__.py  # Recommended

MAX_FILE_SIZE_MB: 1
```
>If you are already using a `.pre-commit-config.yaml` file, simply add the following to your `repos` section:

```yaml
repos:
  - repo: https://github.com/digo5ds/pygitguard
    rev: 1.0.1  # Use the latest tag or release
    hooks:
      - id: pygitguard-scan
        name: PyGitGuard Scan
        entry: pygitguard
        language: system
        types: [python]
        stages: [pre-commit]
```
---

## 💡 Customization Tips

We recommend adding your project’s `<your_project>/__version__.py` file to the `BEST_PRACTICES_FILES` list to track your package version properly.

---

## 🔧 Integration with pre-commit

To use pygitguard as a local hook with [pre-commit](https://pre-commit.com):

```yaml
# .pre-commit-config.yaml
- repo: <your_repo>
  hooks:
    - id: pygitguard
      name: pygitguard
      entry: pygitguard_cli
      language: system
      types: [python]
```

---

## 📄 License

Distributed under the MIT License.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues or submit PRs for enhancements, fixes, or additional patterns.

### 📬 Contact
[LinkedIn profile](https://www.linkedin.com/in/diogosilvaf/).