import utils
import pyautogui
from log_config import configurar_logger

# Configura o logger
logger = configurar_logger("Menu")

logger.info("Iniciando o processo...")

# Solicita ao usuário o texto de pesquisa

texto = pyautogui.prompt(
    text='Digite o que quer achar e em qual cidade:',
    title='Pesquisa de Estabelecimentos',
    default=''
)

if not texto:
    logger.critical("Nenhum texto de pesquisa foi fornecido. Encerrando o programa.")
    logger.info("---------------------------------------------------")
    pyautogui.alert(
        text='Nenhum texto foi fornecido. O programa será encerrado.',
        title='Aviso',
        button='OK'
    )
    exit()

# Chama a função para buscar os lugares na API e obter os resultados

logger.info(f"Iniciando pesquisa Pela API com os seguintes dados: {texto}")
resultado = utils.api_places(texto)
if not resultado:
    logger.critical("A busca na API falhou ou retornou resultados vazios. Encerrando o programa.")
    logger.info("---------------------------------------------------")
    pyautogui.alert(
        text='A busca na API falhou ou retornou resultados vazios. O programa será encerrado.',
        title='Aviso',
        button='OK'
    )
    exit()

logger.info("Pesquisa terminada.")

# Gera o arquivo Excel com os resultados obtidos

logger.info("Gerando arquivo Excel com os resultados...")
utils.gerarexcel(resultado)

# Exibe uma mensagem de conclusão para o usuário
logger.info("Exibindo mensagem de finalização para o usuário.")
pyautogui.alert(
    text='Processo finalizado !',
    title='Aviso',
    button='OK'
)
logger.info("Processo finalizado com sucesso.")
logger.info("---------------------------------------------------")
