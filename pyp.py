#!/usr/bin/env python3

import os
import hashlib
import re
import base64
from pathlib import Path
from pipfile import Pipfile

# taken from pipenv
def virtualenv_name():
    # Replace dangerous characters into '_'. The length of the sanitized
    # project name is limited as 42 because of the limit of linux kernel
    #
    # 42 = 127 - len('/home//.local/share/virtualenvs//bin/python2') - 32 - len('-HASHHASH')
    #
    #      127 : BINPRM_BUF_SIZE - 1
    #       32 : Maximum length of username
    #
    # References:
    #   https://www.gnu.org/software/bash/manual/html_node/Double-Quotes.html
    #   http://www.tldp.org/LDP/abs/html/special-chars.html#FIELDREF
    #   https://github.com/torvalds/linux/blob/2bfe01ef/include/uapi/linux/binfmts.h#L18
    pipfile = Path(Pipfile.find())
    assert pipfile.is_file()
    sanitized = re.sub(r'[ $`!*@"\\\r\n\t]', '_', pipfile.parent.name)[0:42]

    # Hash the full path of the pipfile
    hash = hashlib.sha256(str(pipfile).encode()).digest()[:6]
    encoded_hash = base64.urlsafe_b64encode(hash).decode()

    # If the pipfile was located at '/home/user/MY_PROJECT/Pipfile',
    # the name of its virtualenv will be 'my-project-wyUfYPqE'
    return sanitized + '-' + encoded_hash

def virtualenvs_path():
    return Path('~/.local/share/virtualenvs').expanduser()

def where_env(name=None):
    name = name or virtualenv_name()
    vp = virtualenvs_path()
    return str(vp / name)

def make_env(name=None):
    name = name or virtualenv_name()

    vp = virtualenvs_path()
    env = os.environ.copy()
    env.update({
        'PATH': os.pathsep.join([
            str(vp / name / 'bin'),
            env['PATH']
            ]),
        'VIRTUAL_ENV': str(vp / name)
        })
    # TBH I don't know what these do but pew does it
    env.pop('PYTHONHOME', None)
    env.pop('__PYENV_LAUNCHER__', None)
    return env

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--venv', default=False, action='store_true', help='like pipenv --where')
    parser.add_argument('--name', default=None, help='Virtualenv name')
    parser.add_argument('rest', nargs='*', default=('bash', '--noprofile'))
    args = parser.parse_args()

    if args.where:
        print(where_env(args.name))
    else:
        os.execvpe(args.rest[0], args.rest, make_env(name=args.name))

if __name__ == '__main__':
    main()
