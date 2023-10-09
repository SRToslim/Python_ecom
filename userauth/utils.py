from user_agents import parse


def get_client_ip(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_os_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    user_agent_info = parse(user_agent)

    # OS Information
    os_name = user_agent_info.os.family
    os_version = user_agent_info.os.version_string

    return f"OS: {os_name} {os_version}"


def get_client_browser_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    user_agent_info = parse(user_agent)

    # Browser Information
    browser_family = user_agent_info.browser.family
    browser_version = user_agent_info.browser.version_string

    return f"Browser: {browser_family} {browser_version}"


def get_client_device_info(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')

    user_agent_info = parse(user_agent)

    # Device Information
    device_family = user_agent_info.device.family
    device_brand = user_agent_info.device.brand
    languages = accept_language.split(',')
    primary_language = languages[0].split(';')[0]

    return f"Device: {device_family}-{device_brand}, Language: {primary_language}"