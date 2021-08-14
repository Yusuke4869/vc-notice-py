from typing import Union
import sys

import commons.errors as errors

"""
Change type String to Bool.
String型からBool型への変更.
"""
def str_to_bool(string: str) -> bool:
    return str(string).lower() in ["true", "1", "yes"]

"""
Change type String to Int.
String型からInt型への変更.
"""
def str_to_int(string: str) -> Union[int, bool]:
    try:
        return int(string)
    except ValueError:
        return False
    except Exception as e:
        errors.critical_print(e)
        sys.exit(1)