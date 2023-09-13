import os


def builtin_echo(args) -> None:
    print(" ".join(args))


def builtin_exit(args) -> None:
    print("BYE")
    exit()


def find_command(command):
    if "/" in command:
        return command if os.path.exists(command) else None

    # 環境変数PATHを「:」で分割し，順にコマンドのファイルを探す
    for path in os.environ["PATH"].split(":"):
        path = os.path.join(path, command)
        if os.path.exists(path) and not os.path.isdir(path):
            return path
    return None
