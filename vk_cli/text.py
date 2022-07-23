from colorama import Fore

error = f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}]"
args_error = (f"{error} Wrong arguments."
              f" Use {Fore.CYAN}vk api METHOD NAME=VALUE{Fore.RESET}")

profile_error = f"{error} Profile not found. Use {Fore.CYAN}vk profile new{Fore.RESET}"
