This is a personal tool that accomplishes the same thing that `pipenv shell` does, but without keeping 2 open Python processes open to do so. It also starts much faster which can be nice when you want to run one-off commands in a virtualenv without opening a subshell.

Pipenv uses pexpect to control a pew process that uses Popen to start a subshell. That chain of processes remains alive throughout the lifetime of the shell. Instead I use execvpe to just replace the existing shell.

By default it spawns a bash subshell but you can pass a program to run instead.

```pip install git+https://github.com/aconz2/pyp```
