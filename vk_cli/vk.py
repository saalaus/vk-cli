import requests
from click import ClickException
from rich.console import Group
from rich.panel import Panel
from rich.text import Text


API_URL = "https://api.vk.com/method/"


def color_text(key, value):
    text = Text()
    text.append(key, "blue bold")
    text.append(": ")
    if isinstance(value, bool):
        if value:
            text.append(str(value), "green italic")
        else:
            text.append(str(value), "red italic")
    elif isinstance(value, int) or isinstance(value, float):
        text.append(str(value), "cyan")
    else:
        text.append(value, "dark_green")
    return text


def list_to_panel(lst: list, title: str = ""):
    start_text = f"{title}: [" if title else "["
    if len(lst) == 0:
        return f"{start_text} ]"
    group = Group(start_text)
    for item in lst:
        if isinstance(item, dict):
            value = dict_to_panel(item)
            group.renderables.append(Panel(value))
        elif isinstance(item, list):
            group.renderables.append(list_to_panel(item))
        else:
            group.renderables.append(f"  {item}")
    group.renderables.append("]")
    return group


def dict_to_panel(dictionary: dict):
    group = Group()
    for key, value in dictionary.items():
        if isinstance(value, dict):
            value = dict_to_panel(value)
            group.renderables.append(Panel(value, title=key, title_align="left"))
        elif isinstance(value, list):
            value = list_to_panel(value, key)
            group.renderables.append(value)
        else:
            group.renderables.append(color_text(key, value))
    return group


class RichResponse(dict):
    def __rich_console__(self, console, options):
        if isinstance(self, list):
            yield Panel(list_to_panel(self), title="response")
        elif isinstance(self, dict):
            yield Panel(dict_to_panel(self), title="response")


class VkError(ClickException):
    def __init__(self, response):
        error = response.get("error")
        code = error.get("error_code")
        error_msg = error.get("error_msg")
        if not code and not error_msg:
            message = str(response)
        else:
            message = f"VkApi Error:\n[{code}] - {error_msg}"

        super().__init__(message)
        

def method(method_name, **kwargs) -> dict:
    """
    Call the API method.
    """
    kwargs['v'] = '5.92'
    response = requests.get(API_URL + method_name, params=kwargs).json()
    if "error" in response:
        raise VkError(response)

    return RichResponse(response)
