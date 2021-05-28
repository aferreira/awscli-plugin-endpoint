import warnings

ENDPOINT_URL = 'endpoint_url'
VERIFY_SSL = 'verify_ssl'
CA_BUNDLE = 'ca_bundle'

def str2bool(value):
    return str(value).lower() in ['1', 'yes', 'y', 'true', 'on']

# XXX
def get_attr_from_profile(parsed_args, kwargs, attr):
    session = kwargs['session']
    # Set profile to session so we can load profile from config
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)    
    return _get_attr_from_profile(session.get_scoped_config(), parsed_args.command, attr)

def _get_attr_from_profile(profile, command, attr):
    if command in profile and attr in profile[command]:
        return profile[command][attr]
    return None

def get_endpoint_from_profile(parsed_args, kwargs):
    return get_attr_from_profile(parsed_args, kwargs, ENDPOINT_URL)

def set_endpoint_from_profile(parsed_args, **kwargs):
    if parsed_args.endpoint_url:   # Respect --endpoint-url if present
        return
    
    endpoint_url = get_endpoint_from_profile(parsed_args, kwargs)
    if endpoint_url is not None:
        parsed_args.endpoint_url = endpoint_url

def get_verify_from_profile(parsed_args, kwargs):
    v = get_attr_from_profile(parsed_args, kwargs, VERIFY_SSL)
    if v is None:
        return v
    return str2bool(v)

def set_verify_from_profile(parsed_args, **kwargs):
    if not parsed_args.verify_ssl:   # Respect --no-verify-ssl if present
        return
    
    verify_ssl = get_verify_from_profile(parsed_args, kwargs)
    if verify_ssl is not None:
        parsed_args.verify_ssl = verify_ssl
        if not verify_ssl:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

def get_ca_bundle_from_profile(parsed_args, kwargs):
    return get_attr_from_profile(parsed_args, kwargs, CA_BUNDLE)
#    return profile.get(command, {}).get(CA_BUNDLE)

def set_ca_bundle_from_profile(parsed_args, **kwargs):
    if parsed_args.ca_bundle:   # Respect --ca-bundle if present
        return

    ca_bundle = get_ca_bundle_from_profile(parsed_args, kwargs)
    if ca_bundle is not None:
        parsed_args.ca_bundle = ca_bundle

def awscli_initialize(cli):
    cli.register('top-level-args-parsed', set_endpoint_from_profile)
    cli.register('top-level-args-parsed', set_verify_from_profile)
    cli.register('top-level-args-parsed', set_ca_bundle_from_profile)
