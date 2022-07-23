import requests
from colorama import Fore


def format_vk_error(response):
    """
    Format the error message from VK API.
    """
    error = response['error']
    error_code = f"[{Fore.LIGHTRED_EX}{error['error_code']}{Fore.RESET}]"
    error_msg = error["error_msg"]
    request_params = ""
    for i in error["request_params"]:
        # request_params += "# " + click.style(i["key"], fg="bright_yellow") + " = " + click.style(i["value"], fg="cyan") + "\n"
        request_params += (f"# {Fore.LIGHTYELLOW_EX}{i['key']}{Fore.RESET} = "
                           f"{Fore.CYAN}{i['value']}{Fore.RESET}\n")
    return f"{error_code} {error_msg}\n{request_params}"


API_URL = "https://api.vk.com/method/"
        

def method(method_name, **kwargs) -> dict:
    """
    Call the API method.
    """
    kwargs['v'] = '5.92'
    response = requests.get(API_URL + method_name, params=kwargs)
    return response.json()