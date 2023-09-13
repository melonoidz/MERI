from function import builtin_echo, builtin_exit

BUILTIN_COMMAND_FUNC_MAPPING: dict = {
    "echo": builtin_echo,
    "exit": builtin_exit,
}
