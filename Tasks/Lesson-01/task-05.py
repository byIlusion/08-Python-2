import subprocess


def subproc(args):
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in subproc_ping.stdout:
        line = line.decode('cp866')
        print(line, end='')


if __name__ == '__main__':
    args = ['ping', 'youtube.com', '-n', '3']
    print(f'\n\nВыполняется команда: > {" ".join(args)}')
    subproc(args)

    args = ['ping', 'yandex.ru', '-n', '3']
    print(f'\n\nВыполняется команда: > {" ".join(args)}')
    subproc(args)
