# VK CLI
Call VK API methods from terminal.

## Installation

Install with pip

```bash
  pip install vk-cli
```
    
## Usage
Help
```bash
> vk -h
Usage: python -m vk [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  api      Call the API
  profile  Proile commands
  shell    start shell
```
Create new profile
```bash
vk profile new --access-token <VK TOKEN>
```

API call
```bash
vk api users.get user_id=1
```



## Shell
Run Shell
```bash
vk shell
```
Shel is it interactive python shell, but you can call to api vk
```python
>>> response = API.users.get(user_id=1)
>>> user = user["response"][0]
>>> print(user["first_name"], user["last_name"], sep=" ")
Павел Дуров
```