from twisted.internet import defer, utils


@defer.inlineCallbacks
def execute_shell_command(command):
    _, _, code = yield utils.getProcessOutputAndValue('/bin/bash', args=['-c', command])
    defer.returnValue(code)

def version_notation_pip_to_soup(pip_notation):
    if pip_notation[:2] == '==':
        return pip_notation[2:]
    elif pip_notation[:2] == '>=':
        return '+{0}'.format(pip_notation[2:])
    elif pip_notation[:1] == '>':
        return '+{0}'.format(pip_notation[1:])
    elif pip_notation[:2] == '<=':
        return '-{0}'.format(pip_notation[2:])
    elif pip_notation[:1] == '<':
        return '-{0}'.format(pip_notation[1:])
    else:
        return '*'

def version_notation_soup_to_pip(soup_notation):
    if soup_notation[:1] == '+':
        return '>={0}'.format(soup_notation[1:])
    elif soup_notation[:1] == '-':
        return '<={0}'.format(soup_notation[1:])
    elif soup_notation == '*':
        return ''
    else:
        return '=={0}'.format(soup_notation)
