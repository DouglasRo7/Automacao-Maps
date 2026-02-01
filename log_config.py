import logging
import os

# Configuração dos logs

def configurar_logger(nome_logger="app"):
    logger = logging.getLogger(nome_logger)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    pasta_script = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(pasta_script, "automation.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
