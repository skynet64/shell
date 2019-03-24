import os


def init(cmd):
    """Add new commands to commands dictionary"""
    cmd.update({'export': export,
                'unset': unset,
                'echo': echo})


def export(args, stdin, stdout, stderr):
    """Change / show environment variables"""
    if len(args) > 2:
        os.environ.update({args[1]: args[2]})
    elif len(args) > 1:
        if args[1] in os.environ.keys():
            stdout.write(os.environ[args[1]] + '\n')
        else:
            stderr.write('Invalid argument\n')
    else:
        for var in os.environ.items():
            stdout.write(var[0] + '=' + var[1] + '\n')


def unset(args, stdin, stdout, stderr):
    """Remove environment variable"""
    if len(args) > 1:
        del os.environ[args[1]]
    else:
        stderr.write('Invalid argument\n')


def echo(args, stdin, stdout, stderr):
    """Print specified string or variable value"""
    for i in range(1, len(args)):
        if args[i][0] == '$' and args[i][1:] in os.environ.keys():
            stdout.write(os.environ[args[i][1:]] + ' ')
        else:
            stdout.write(args[i] + ' ')
    stdout.write('\n')
