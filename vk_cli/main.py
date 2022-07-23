import json
import click
from .profile import delete_profile, list_profiles, load_profile, new_profile, yield_all_profile
from .vk import method, format_vk_error
from pprint import pformat
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from colorama import Fore
from . import text
from .shell import run_shell


@click.group()
@click.help_option("--help", "-h")
def command():
    ...

    
@command.command()
@click.argument("method_name")
@click.argument('args', nargs=-1)
@click.option("--profile", "-p", type=click.INT, default=0,
              help="Profile to use", show_default=True)
@click.option("--pass-response", "-pr", is_flag=True, default=False,
              help="Pass response")
@click.option("--pretty-print", "-pp", is_flag=True, default=True,
              help="Disable pretty print", show_default=True)
# @click.option("--execute", "-e", type=click.File('r'),
#               help="Execute code from file")
@click.help_option("--help", "-h")
def api(method_name, args, profile, pass_response, pretty_print):
    "Call the API"
    try:
        args = {i.split("=")[0]: i.split("=")[1] for i in args}
    except IndexError:
        click.echo(text.args_error)
        return
    profile = load_profile(f"{profile}.profile")
    if not profile:
        click.echo(text.profile_error)
        return
    args.update(access_token=profile["access_token"])
    response = method(method_name, **args)
    if "error" in response and pretty_print:
        return click.echo(format_vk_error(response))
    elif "response" in response and pass_response:
        response =  response["response"]
        if isinstance(response, type([])) and len(response) == 1:
            response = response[0]
    if pretty_print:
        response = pformat(response)
        response = highlight(response, PythonLexer(), TerminalFormatter())
    return click.echo(response)


@command.command()
@click.option("--profile", "-p", type=click.INT, default=0,
              help="Profile to use")
@click.help_option("--help", "-h")
def shell(profile):
    "start shell"
    run_shell(profile)
    
    
@command.group()
@click.help_option("--help", "-h")
def profile():
    "Proile commands"

    
@profile.command()
@click.help_option("--help", "-h")
@click.option("--access-token", prompt="Your access token", help="access token", hide_input=True)
def new(access_token):
    "New profile"
    user = method("users.get", access_token=access_token)
    if "response" not in user:
        click.echo("Error while check token. Please, check your access token.")
        return
    user = user["response"][0]
    name = f"{user['first_name']} {user['last_name']}"
    data = dict(access_token=access_token, name=name, id=user['id'])
    profile_n = new_profile(data)
    click.echo(f"Your profile save as {profile_n}")


@profile.command()
@click.help_option("--help", "-h")
def list():
    "List your profiles"
    all_profiles = list_profiles()
    text = ""
    for profile in yield_all_profile():
        user = method("users.get", access_token=profile["access_token"])
        if "error" in user:
            check = f"{Fore.LIGHTRED_EX}Invalid{Fore.RESET}"
        else:
            check = f"{Fore.LIGHTGREEN_EX}Valid{Fore.RESET}"
        text += (f"Profile: {Fore.LIGHTYELLOW_EX}{profile['number']}{Fore.RESET}\n"
                 f"  Name: {Fore.CYAN}{profile['name']}{Fore.RESET}\n"
                 f"  Status: {check}\n\n")
    click.echo(text)
        


@profile.command()
@click.argument("profile_number", type=click.INT)
@click.help_option("--help", "-h")
def delete(profile_number):
    "Delete your profile"
    profile_n = load_profile(f"{profile_number}.profile")
    if not profile_n:
        click.echo(f"{Fore.RED}Profile not found{Fore.RESET}")
        return
    click.echo(f"Delete profile {profile_n['number']}")
    delete_profile(profile_n["number"])

if __name__ == "__main__":
    command()