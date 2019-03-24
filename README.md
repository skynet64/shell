# Shell

Created by Dmitry Ryabkov Group Б05-812

### Launch
Start command: `python3 shell.py`.
### Supported commands

1. cd

    Changes working directory.

    Syntax: `cd directory_name`.

2. pwd

    Prints path to current working directory.

    Syntax: `pwd`.

3. ls

    Prints all files in directory.

    Syntax: `ls [-a] [-l] [directory_name]`.

    Parameter `-a` prints all files including files that starts with '.' (except for '.' and '..').

    Parameter `-l` also prints sizes of files and their type.

4. mkdir

    Creates new directory.

    Syntax: `mkdir directory_name`.

5. rmdir

    Removes directory.

    Syntax: `rmdir [-r] directory_name`.

    Parameter `-r`  removes all content of a directory recursively

6. cp

    Copies file / directory.

    Syntax: `cp source destination`.

7. mv

    Moves file / directory.

    Syntax: `mv source destination`.

8. rm

    Removes file.

    Syntax: `rm file_name`.

9. export

    Changes / shows environment variables.

    Syntax: `export [variable] [value]`.

    If 2 parameters are passed then it assigns `value` to `variable`.

    If 1 parameter is passed then it shows value of `variable`.

    If 0 parameters are passed then it shows all variables and their values.

10. unset

    Removes environment variable.

    Syntax: `unset variable`.

11. echo

    Prints specified string or variable value.

    Syntax: `echo param1 param2 ...`.

    If parameter starts with '$' then it tries to print value of variable.

12. Running programs

    Syntax: `prog_name param1 param2 ...`.

### Input / Output redirection

Syntax: `cmd1 params1 | cmd2 params2 | ... | cmdN paramsN [< input] [>|1>|>>|1>> output] [>|2>|>>|2>> error]`.

Passes output from `cmd1` to `cmd2` and etc.

Sets stdin for `cmd1` as `input`.

Sets stdout for `cmdN` as `output`.

Sets stderr for all commands as `error`.

If used `>>` instead of `>` then file will not be overwritten but will be appended.

IO redirection operators (`>` `>>` `1>` `1>>` `2>` `2>>`) must be after the last `|`.
