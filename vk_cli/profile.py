import pickle
import os
from pathlib import Path


PROFILES_DIR = Path("profiles/")
PROFILES_DIR.mkdir(exist_ok=True)


def _generater_profile_id():
    profiles = list_profiles()
    try:
        if len(profiles) <= 0:
            return "0"
        profile_count = max([int(profile) for profile in profiles]) + 1
        return str(profile_count)
    except ValueError:
        raise ValueError("There was an error when generating the profile ID, please use the"
                         " --name option to explicitly specify the name of the profile")


def list_profiles():
    return [file.stem for file in PROFILES_DIR.glob("*.profile")]


def load_profile(profile_name):
    file = PROFILES_DIR / f"{profile_name}.profile"

    if file.exists():
        with open(file, "rb") as f:
            return pickle.load(f)
    else:
        return None


def new_profile(data: dict, profile_name: str = None):
    if profile_name is None:
        profile_name = _generater_profile_id()

    data.update(number=profile_name)
    file = PROFILES_DIR / f"{profile_name}.profile"
    with open(file, "wb") as f:
        pickle.dump(data, f)
    return profile_name


def delete_profile(profile_name: str):
    file = PROFILES_DIR / f"{profile_name}.profile"
    return file.unlink(missing_ok=True)