import warnings

ENDPOINT_URL = 'endpoint_url'
VERIFY_SSL = 'verify_ssl'
CA_BUNDLE = 'ca_bundle'

def str2bool(value):
    return str(value).lower() in ['1', 'yes', 'y', 'true', 'on']

# XXX
def get_attr_from_profile(profile, command, attr):
    if command in profile and attr in profile[command]:
        return profile[command][attr]
    return None

def get_verify_from_profile(profile, command):
    v = get_attr_from_profile(profile, command, VERIFY_SSL)
    return v if v is None else str2bool(v)
#    verify = True
#    if command in profile:
#        if VERIFY_SSL in profile[command]:
#            verify = str2bool(profile[command][VERIFY_SSL])
#    return verify

def get_ca_bundle_from_profile(profile, command):
    return get_attr_from_profile(profile, command, CA_BUNDLE)
#    return profile.get(command, {}).get(CA_BUNDLE)

def get_endpoint_from_profile(profile, command):
    return get_attr_from_profile(profile, command, ENDPOINT_URL)
#    endpoint = None
#    if command in profile:
#        if ENDPOINT_URL in profile[command]:
#            endpoint = profile[command][ENDPOINT_URL]
#    return endpoint

def set_endpoint_from_profile(parsed_args, **kwargs):
    if parsed_args.endpoint_url:   # If endpoint set on CLI option, use CLI endpoint
        return
    
    session = kwargs['session']
    # Set profile to session so we can load profile from config
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)
    service_endpoint = get_endpoint_from_profile(session.get_scoped_config(), parsed_args.command)
    if service_endpoint is not None:
        parsed_args.endpoint_url = service_endpoint

def set_verify_from_profile(parsed_args, **kwargs):
    verify_ssl = parsed_args.verify_ssl
    # By default verify_ssl is set to true
    # if --no-verify-ssl is specified, parsed_args.verify_ssl is False
    # so keep it
    if verify_ssl:
        session = kwargs['session']
        # Set profile to session so we can load profile from config
        if parsed_args.profile:
            session.set_config_variable('profile', parsed_args.profile)
        service_verify = get_verify_from_profile(session.get_scoped_config(), parsed_args.command)
        if service_verify is not None:
            parsed_args.verify_ssl = service_verify
            if not service_verify:
                warnings.filterwarnings('ignore', 'Unverified HTTPS request')

def set_ca_bundle_from_profile(parsed_args, **kwargs):
    if parsed_args.ca_bundle is not None: # Respect command line arg if present
        return

    session = kwargs['session']
    # Set profile to session so we can load profile from config
    if parsed_args.profile:
        session.set_config_variable('profile', parsed_args.profile)
    parsed_args.ca_bundle = get_ca_bundle_from_profile(session.get_scoped_config(), parsed_args.command)

def awscli_initialize(cli):
    cli.register('top-level-args-parsed', set_endpoint_from_profile)
    cli.register('top-level-args-parsed', set_verify_from_profile)
    cli.register('top-level-args-parsed', set_ca_bundle_from_profile)
