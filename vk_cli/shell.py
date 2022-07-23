import code
import sys

from .vk import method
from .profile import load_profile
from colorama import Fore
import colorama
from . import text


class API:
    def __init__(self, method=None):
        self.method = method
    def __getattr__(self, name):
        return type(self)(
            self.method + "." + name if self.method else name
        )
    def __call__(self, **kwargs):
        if "access_token" not in kwargs:
            if not profile:
                raise ValueError("Not acces token passed and not profile")
            kwargs.update(access_token=profile["access_token"])
        return method(self.method, **kwargs)


colorama.init()
API = API()
profile = None


def run_shell(profile_num):
    global profile
    profile = load_profile(f"{profile_num}.profile")
    if not profile:
        print(text.profile_error)
        return 
    starting = (f"Python {sys.version}\n"
                f"Type \"{Fore.CYAN}help{Fore.RESET}\", "
                f"\"{Fore.CYAN}copyright{Fore.RESET}\" or "
                f"\"{Fore.CYAN}license{Fore.RESET}\" for more information."
                f"\nVK API: use {Fore.CYAN}API.METHOD_NAME{Fore.RESET}"
                 " to call API\n"
                f"Example: {Fore.CYAN}API.users.get(user_ids=1){Fore.RESET}")
    exiting = ""
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact(starting, exiting)
