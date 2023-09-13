import getpass
import os
import sys

from .function import find_command
from .mapping import BUILTIN_COMMAND_FUNC_MAPPING


def main() -> None:
    print(f"HI! {getpass.getuser().upper()}")
    print(f"YOUR PC LANG IS {os.environ['LANG']}")
    while True:
        line = input("> ")
        tokens = line.split()
        if len(tokens) == 0:
            continue

        command = tokens[0]
        args = tokens[1:]

        if command in BUILTIN_COMMAND_FUNC_MAPPING:
            # 内部コマンド
            func = BUILTIN_COMMAND_FUNC_MAPPING[command]
            func(args)
        else:
            # 外部コマンド
            # PATHで設定されたディレクトリにあるファイル
            command_path = find_command(command)

            if command_path is None:
                print(f"{command} :COMMAND NOT FOUND!", file=sys.stderr)
                continue

            # folk・execの実装
            # 子プロセスを作成
            # システムコールを使って，カーネルにプロセスを実行してもらう
            pid = os.fork()

            if pid < 0:
                print("FORK FAILED", file=sys.stderr)
            elif pid == 0:
                # 子プロセスの処理
                cmd_basename = os.path.basename(command_path)
                os.execve(command_path, [cmd_basename] + args, os.environ)
            else:
                # 親プロセスが，子プロセスの終了を待つ
                # ゾンビプロセス対策
                os.waitpid(pid, 0)


main()
