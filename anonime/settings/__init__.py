from decouple import config
from .base import *

if config('DEBUG', cast=bool) == True:
    from .local import *
else:
    from .production import *