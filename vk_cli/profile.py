import pickle
import os

def create_profiles_folder():
    if not os.path.isdir("profiles"):
        os.mkdir("profiles")


def list_profiles():
    return [i for i in os.listdir("profiles") if i.endswith("profile")]


def load_profile(n):
    try:
        return pickle.load(open(f"profiles/{n}", "rb"))
    except FileNotFoundError:
        return False


def yield_all_profile():
    for i in list_profiles():
        yield load_profile(i)


def new_profile(profile_data):
    create_profiles_folder()
    dir = list_profiles()
    if dir:
        profile_count = max([int(i.split(".")[0]) for i in dir]) + 1
    else:
        profile_count = 0
    profile_data.update(number=profile_count)
    pickle.dump(profile_data, open(f"profiles/{profile_count}.profile", "wb"))
    return profile_count


def delete_profile(profile_number):
    return os.remove(f"profiles/{profile_number}.profile")