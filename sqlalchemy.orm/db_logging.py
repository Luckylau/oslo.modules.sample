from oslo_config import cfg
from oslo_log import log as logging

def logname(name):
    return logging.getLogger(name)

def rpc_log_prepare(DOMAIN):
    logging.register_options(cfg.CONF)
    extra_log_level_defaults=[
        'dogpile=INFO',
        'routes=INFO'
    ]
    logging.set_defaults(default_log_levels=logging.get_default_log_levels()+extra_log_level_defaults)
    logging.setup(cfg.CONF,DOMAIN)
