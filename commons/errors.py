import sys

from commons.log import Log
log = Log()

"""
Print Error (Level: ERROR)
エラー出力 (レベル: ERROR)
"""
def error_print(exception) -> None:
    try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filepath = exc_tb.tb_frame.f_code.co_filename
        content = f"File {filepath}, line {exc_tb.tb_lineno}, {exception.__class__.__name__}: {exc_obj}"
        log.print_error_log(content)
    except:
        pass

"""
Print Error (Level: CRITICAL)
エラー出力 (Level: CRITICAL)
"""
def critical_print(exception) -> None:
    try:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filepath = exc_tb.tb_frame.f_code.co_filename
        content = f"File {filepath}, line {exc_tb.tb_lineno}, {exception.__class__.__name__}: {exc_obj}"
        log.print_critical_log(content)
    except:
        pass

class BotError(Exception):
    pass

class TokenNotFoundError(BotError):
    pass