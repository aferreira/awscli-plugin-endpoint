import warnings
import logging

from awscli.clidriver import LOG_FORMAT, LOG

logger = logging.getLogger(__name__)

ENDPOINT_URL = 'endpoint_url'
VERIFY_SSL = 'verify_ssl'
CA_BUNDLE = 'ca_bundle'

def str2bool(value):
    return str(value).lower() in ['1', 'yes', 'y', 'true', 'on']

def get_arg_from_profile(parsed_args, session, arg_name):
    # Set profile to session so we can load profile from config
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)    
    return _get_arg_from_profile(session.get_scoped_config(), parsed_args.command, arg_name)

def _get_arg_from_profile(profile, command, arg_name):
    if command in profile and arg_name in profile[command]:
        return profile[command][arg_name]
    if "DEFAULT" in profile and arg_name in profile["DEFAULT"]:   # XXX
        return profile[arg_name]
    return None

def set_endpoint_from_profile(parsed_args, session, **kwargs):
    if parsed_args.endpoint_url:   # Respect --endpoint-url if present
        return
    
    endpoint_url = get_arg_from_profile(parsed_args, session, ENDPOINT_URL)
    if endpoint_url is not None:
        parsed_args.endpoint_url = endpoint_url
        LOG.debug("endpoint_url = {}".format(parsed_args.endpoint_url)) # DEBUG

def set_verify_from_profile(parsed_args, session, **kwargs):
    if not parsed_args.verify_ssl:   # Respect --no-verify-ssl if present
        return
    
    verify_ssl = get_arg_from_profile(parsed_args, session, VERIFY_SSL)
    if verify_ssl is not None:
        parsed_args.verify_ssl = str2bool(verify_ssl)
        logger.debug("verify_ssl = {}".format(parsed_args.verify_ssl))
        if not parsed_args.verify_ssl:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

def set_ca_bundle_from_profile(parsed_args, session, **kwargs):
    if parsed_args.ca_bundle:   # Respect --ca-bundle if present
        return

    ca_bundle = get_arg_from_profile(parsed_args, session, CA_BUNDLE)
    if ca_bundle is not None:
        parsed_args.ca_bundle = ca_bundle
        logger.debug("ca_bundle = {}".format(parsed_args.ca_bundle))
                                
def debug_plugin(parsed_args, session, **kwargs):
    session.set_stream_logger(__name__, logging.DEBUG, format_string=LOG_FORMAT)
    LOG.info("HERE")
    warn.warn("HERE")
    
def awscli_initialize(cli):
    LOG.info("HERE at awscli_plugin_endpoint.awscli_initialize")
    cli.register('top-level-args-parsed', debug_plugin)
    cli.register('top-level-args-parsed', set_endpoint_from_profile)
    cli.register('top-level-args-parsed', set_verify_from_profile)
    cli.register('top-level-args-parsed', set_ca_bundle_from_profile)
