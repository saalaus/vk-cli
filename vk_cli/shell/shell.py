import code
import sys
from enum import Enum

from vk_cli.vk import method
from vk_cli.profile import load_profile
from rich import print
from vk_cli import text


class ShellType(str, Enum):
    default = "default"
    ipython = "ipython"


class API:
    def __init__(self, method_name=None):
        self.method_name = method_name

    def __getattr__(self, name):
        return type(self)(
            self.method_name + "." + name if self.method_name else name
        )

    def __call__(self, **kwargs):
        if "access_token" not in kwargs:
            if not profile:
                raise ValueError("Not acces token passed and not profile")
            kwargs.update(access_token=profile["access_token"])
        return method(self.method_name, **kwargs)


API = api = API()
profile = {}


def run_shell(profile_num=None, shell=None):
    global profile
    starting = (f"Python {sys.version}\n"
                f"Type \"[cyan]help[/cyan]\", "
                f"\"[cyan]copyright[/cyan]\" or "
                f"\"[cyan]license[/cyan]\" for more information."
                f"\nVK API: use [cyan]API.METHOD_NAME[/cyan]"
                f" to call API\n"
                f"Example: [cyan]API.users.get(user_ids=1)[/cyan]")
    exiting = ""
    variables = globals().copy()
    variables.update(locals())

    if profile_num is not None:
        profile = load_profile(profile_num)
        if not profile:
            print(text.profile_error)
    print(starting)
    if shell is None:
        try:
            from IPython import embed

            embed(header="")
        except ImportError:
            shell = code.InteractiveConsole(variables)
            shell.interact("", "")
    else:
        if shell == ShellType.default:
            shell = code.InteractiveConsole(variables)
            shell.interact("", "")
        elif shell == ShellType.ipython:
            from IPython import embed
            embed(header="")
    print(exiting)
