import logging

# Códigos ANSI para cores por nível
COLOR_CODES = {
    "DEBUG": "\033[36m",  # cyan
    "INFO": "\033[1;32m",  # bold green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[1;31m",  # bold red
}
RESET_CODE = "\033[0m"

# Ícones por nível
ICONS = {
    "DEBUG": "🐛",
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "💀",
}


class IconOnlyColorFormatter(logging.Formatter):
    def format(self, record):
        # Substitui completamente o levelname por um ícone
        level = record.levelname
        record.levelname = ICONS.get(level, "")

        # Formata a mensagem normalmente
        msg = super().format(record)

        # Aplica cor ANSI à linha inteira
        color = COLOR_CODES.get(level, "")
        return f"{color}{msg}{RESET_CODE}"


# Configuração básica do logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s  %(name)s -> %(message)s",
    handlers=[logging.StreamHandler()],
)

# Substitui o formatter padrão pelo personalizado
handler = logging.getLogger().handlers[0]
handler.setFormatter(IconOnlyColorFormatter(handler.formatter._fmt))

# Logger de exemplo
logger = logging.getLogger("PYGITGUARD")
