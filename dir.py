import os
import shutil


def init(cmd):
    """Add new commands to commands dictionary"""
    cmd.update({'cd': changeDirectory,
                'pwd': printWDirectory,
                'ls': listDirectory,
                'mkdir': makeDirectory,
                'rmdir': removeDirectory})


def changeDirectory(args, stdin, stdout, stderr):
    """Change working directory"""
    if len(args) > 1:
        try:
            os.chdir(path=args[1])
            if 'PWD' in os.environ.keys():
                os.environ['PWD'] = os.getcwd()
        except Exception as e:
            stderr.write(e.__str__() + '\n')


def printWDirectory(args, stdin, stdout, stderr):
    """Print path to current working directory"""
    stdout.write(os.getcwd() + '\n')


def listDirectory(args, stdin, stdout, stderr):
    """Print all files in directory"""
    print_list = '-l' in args
    while '-l' in args:
        del args[args.index('-l')]

    print_all = '-a' in args
    while '-a' in args:
        del args[args.index('-a')]

    if len(args) > 1:
        path = args[1]
    else:
        path = '.'

    try:
        if print_list:
            with os.scandir(path=path) as dir_ls:
                stdout.write('Size\tName\n')
                for file in dir_ls:
                    if not file.name.startswith('.') or print_all:
                        if file.is_dir():
                            stdout.write('<DIR>\t')
                        elif file.is_symlink():
                            stdout.write('<LINK>\t')
                        else:
                            stdout.write(str(file.stat().st_size) + '\t')
                        stdout.write(file.name + '\n')
        else:
            dir_ls = os.listdir(path=path)
            for file in dir_ls:
                if not file.startswith('.') or print_all:
                    stdout.write(file + ' ')
            stdout.write('\n')
    except Exception as e:
        stderr.write(e.__str__() + '\n')


def makeDirectory(args, stdin, stdout, stderr):
    """Create new directory"""
    if len(args) > 1:
        try:
            os.mkdir(args[1], 0o755)
        except Exception as e:
            stderr.write(e.__str__() + '\n')
    else:
        stderr.write('No directory name specified\n')


def removeDirectory(args, stdin, stdout, stderr):
    """Remove directory"""
    full_del = '-r' in args
    while '-r' in args:
        del args[args.index('-r')]

    if len(args) > 1:
        try:
            if full_del:
                shutil.rmtree(args[1])
            else:
                os.rmdir(args[1])
        except Exception as e:
            stderr.write(e.__str__() + '\n')
    else:
        stderr.write('No directory name specified\n')
