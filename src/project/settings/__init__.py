import os
from .base_settings import *
if os.getenv('PROJECT_ENVIRONMENT') == 'prod':
   from .prod_settings import *
else:
   from .dev_settings import *