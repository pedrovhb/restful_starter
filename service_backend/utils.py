import logging
import sys

JWT_SECRET = 'secret'

log = logging.getLogger('service_backend')
log.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
