from typing import Optional

import typer
from click import BadArgumentUsage
from rich import print as pprint
from rich.panel import Panel
from rich.progress import track

from vk_cli.profile import new_profile, list_profiles, load_profile, delete_profile
from vk_cli.shell.shell import ShellType, run_shell
from .vk import method, VkError, RichResponse

app = typer.Typer(pretty_exceptions_show_locals=False)
profile = typer.Typer()
app.add_typer(profile, name="profile")


@app.command("api")
def api(method_name: str = typer.Argument(..., show_default=False),
        args: Optional[list[str]] = typer.Argument(None, show_default=False),
        profile: int = typer.Option(0),
        raw_response: bool = typer.Option(False, "--raw-response", "-rs", help="Raw response, without pretty print")):
    """Call VK APi

    Example:

        vk api users.get - get current user

        vk api users.search q="Pavel Durov" - search user
    """
    try:
        kwargs = {i.split("=", maxsplit=1)[0]: i.split("=", maxsplit=1)[1] for i in args}
    except IndexError:
        raise BadArgumentUsage("Bad arguments, use name=value, example:\n"
                               "vk api users.search count=1 q=\"Pavel Durov\"")
    current_profile = load_profile(profile)
    kwargs.update(access_token=current_profile["access_token"])

    response = method(method_name, **kwargs)
    if raw_response:
        print(response)
        return

    if "response" in response:
        response = response["response"]
        if isinstance(response, list) and len(response) == 1:
            response = response[0]

    pprint(RichResponse(response))


@app.command("shell", help="Run shell")
def shell(profile_id: int = typer.Option(0, "--profile", show_default=False, help="Profile ID"),
          force_shell: ShellType = typer.Option(None, "--force-shell", "-fs",
                                                help="Which shell to use. Options:\n"
                                                     "default - default python interactive console.\n"
                                                     "ipython - ipython interactive shell")
          ):
    run_shell(profile_id, force_shell)


@profile.command("new", help="Create a new profile.")
def new(access_token: str = typer.Option("", show_default=False, help="Your access_token, "
                                                                      "if not entered, will prompt for user input")):
    if not access_token:
        access_token = typer.prompt("Enter your access token")

    try:
        user = method("users.get", access_token=access_token)["response"][0]
    except VkError as error:
        raise ValueError("An error occurred during token verification. Please check your token") from error

    name = f"{user['first_name']} {user['last_name']}"
    data = dict(access_token=access_token, name=name, id=user["id"])
    profile_n = new_profile(data)
    print(f"Your profile save as {profile_n}")


@profile.command("list", help="Get profile list")
def profiles_list():
    for profile_id in track(list_profiles(), "Checking profiles...", show_speed=False, transient=True):
        current_profile = load_profile(profile_id)
        text = (f"ID: [bold blue]{current_profile['id']}[/bold blue]\n"
                f"Name: [bold]{current_profile['name']}[/bold]")
        try:
            method("users.get", access_token=current_profile["access_token"])
            panel = Panel.fit(text, title=str(current_profile['number']),
                              subtitle="VALID", border_style="green")
        except VkError:
            panel = Panel.fit(text, title=str(current_profile['number']),
                              subtitle="INVALID", border_style="red")

        pprint(panel)


@profile.command("delete", help="Delete profile")
def profile_delete(profile_id: int = typer.Argument(0, help="Profile to delete")):
    delete_profile(str(profile_id))
    print("Successfull delete")


if __name__ == "__main__":
    app()
