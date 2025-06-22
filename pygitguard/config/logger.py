"Custom logging formatter for PYGITGUARD"

import logging

# Colors ANSI
COLOR_CODES = {
    "DEBUG": "\033[36m",  # cyan
    "INFO": "\033[1;32m",  # bold green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[1;31m",  # bold red
}
RESET_CODE = "\033[0m"

# Icons for log levels
ICONS = {
    "DEBUG": "🐛",
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "💀",
}


class IconOnlyColorFormatter(logging.Formatter):
    """ "
    A custom logging formatter that replaces the log level name
    with an icon and applies ANSI color codes to the entire log message.

    This formatter modifies the log record to display an icon corresponding
    to the log level instead of the textual level name.
    It also colors the entire log message line based on the log level
    using ANSI escape codes.

    Attributes
    None

    Methods
    format(record)
        Formats the specified log record, replacing the level name
        with an icon and coloring the message line.
    """

    def format(self, record):
        """
        Formats a logging record by replacing the level name
        with an icon and applying ANSI color codes.

        The method modifies the log record to display
        an icon corresponding to the log level instead
        of the level name. It also applies an ANSI color
        to the entire message line based on the log level.

        Parameters
        ----------
        record : logging.LogRecord
            The log record to be formatted.

        Returns
        -------
        str
            The formatted log message with an icon and color.
        """

        level = record.levelname
        record.levelname = ICONS.get(level, "")

        # Formata a mensagem normalmente
        msg = super().format(record)

        # Aplica cor ANSI à linha inteira
        color = COLOR_CODES.get(level, "")
        return f"{color}{msg}{RESET_CODE}"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s  %(name)s -> %(message)s",
    handlers=[logging.StreamHandler()],
)

handler = logging.getLogger().handlers[0]
handler.setFormatter(IconOnlyColorFormatter(handler.formatter._fmt))

# Logger de exemplo
logger = logging.getLogger("PYGITGUARD")
logger.setLevel(logging.INFO)
