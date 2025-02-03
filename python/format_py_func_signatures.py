import argparse 
import ast 
import astunparse
import tokenize
from typing import List
from rich import print

from fpath_linerange_to_str import fpath_linerange_to_str
from astm_to_linerange import astm_to_linerange
from pyfpath_funcname_to_signature_linerange import pyfpath_funcname_to_signature_linerange
from pyfpath_to_funcnames import pyfpath_to_funcnames
from pyfpath_funcname_to_astm import pyfpath_funcname_to_astm
from replace_fpath_linerange import replace_fpath_linerange

# 
testing = False

def subscript_to_typestr(annotation: ast.Subscript) -> str:
    # 
    if not isinstance(annotation, ast.Subscript):
        raise TypeError(type(annotation))
    
    # 
    if isinstance(annotation.slice, ast.Name):
        outer = annotation.value.id
        inner = annotation.slice.id
        return f"{outer}[{inner}]"

    # 
    if isinstance(annotation.slice, ast.Tuple):
        outer = annotation.value.id
        inner = ', '.join([
            arg_to_typestr(elem)
            for elem in annotation.slice.elts
        ]) 
        complete = f"{outer}[{inner}]"
        return complete

    raise NotImplementedError(type(annotation.slice)) 

def arg_to_typestr(f: ast.arg) -> str:

    if not isinstance(f, (ast.arg, ast.Constant, ast.Subscript, ast.Call)):
        raise TypeError(type(f))

    if isinstance(f, ast.Subscript):
        return subscript_to_typestr(f)
    
    if isinstance(f, ast.Constant) and f.value == None:
        return 'None'
    if isinstance(f, ast.Call):
        return astunparse.unparse(f).strip()
    if isinstance(f.annotation, type(None)):
        return 'type'
    if isinstance(f.annotation, ast.Name):
        out = f.annotation.id
        return out
    if isinstance(f.annotation, ast.Subscript):
        out = subscript_to_typestr(f.annotation)
        return out
    if isinstance(f.annotation, ast.Attribute):
        m = f.annotation.value.id
        a = f.annotation.attr
        return f'{m}.{a}'
    
    raise NotImplementedError(dir(f.annotation), astunparse.unparse(f), type(f.annotation))

def fm_to_args(f: ast.Module) -> dict:
    # 
    num_posargs = len(f.args.args) - len(f.args.defaults)
    num_kwargs  = len(f.args.defaults)
#     print(dir(f.args))
#     print('num args', f.name, num_posargs, num_kwargs)
#     print('unparse f.args', astunparse.unparse(f.args))
#     print('unparse f.args.kwonlyargs', astunparse.unparse(f.args.kwonlyargs))
#     print('unparse f.args.kw_defaults', astunparse.unparse(f.args.kw_defaults))
#     print('unparse f.args.defaults', astunparse.unparse(f.args.defaults))
#     print(f.args.kwonlyargs, f.args.kw_defaults)

    # 
    if len(f.args.kwonlyargs) != len(f.args.kw_defaults):
        raise Exception()

    # 
    posargs     = [
        {
            'def'    : f.args.args[i],
            'default': None,
            'type'   : arg_to_typestr(f.args.args[i])
        } 
        for i in range(num_posargs)
    ]
    kwargs      = [
        {
            'def'    : name_def,
            'default': default_def,
            'type'   : arg_to_typestr(name_def)
        }
        for name_def, default_def in zip(f.args.kwonlyargs, f.args.kw_defaults)
    ]
    kwargs     += [
        {
            'def'    : f.args.args[num_posargs + i],
            'default': f.args.defaults[i],
            'type'   : arg_to_typestr(f.args.args[num_posargs + i])
        }
        for i in range(num_kwargs)
    ]

    return {
        'posargs': posargs,
        'kwargs' : kwargs
    }

def function_to_argsstr_old(f: ast.Module) -> str:
    # 
    args      = fm_to_args(f)
    posargs   = args['posargs']
    kwargs    = args['kwargs']

    # 
    if len(posargs) == 0 and len(kwargs) == 0:
        return "()"
    
    # 
    if len(posargs) == 1 and len(kwargs) == 0:
        argname = posargs[0]['def'].arg
        argtype = posargs[0]['type']
        argstr  = f"{argname}: {argtype}"
        return f"({argstr})"

    # 
    if len(posargs) == 0 and len(kwargs) == 1:
        argname    = kwargs[0]['def'].arg
        argtype    = kwargs[0]['type']
        argdefault = astunparse.unparse(kwargs[0]["default"]).strip()
        argstr     = f"{argname}: {argtype} = {argdefault}"
        return f"({argstr})"
    
    #
    if len(posargs) + len(kwargs) > 1:

        # 
        max_name_len       = max([len(argstruct['def'].arg) for argstruct in posargs] + [len(kwarg['def'].arg) for kwarg in kwargs])
        max_annotation_len = max(
            [
                len(posarg['type']) 
                for posarg in posargs
            ] + [
                len(kwarg['type']) 
                for kwarg in kwargs
            ] + [0]
        )
        
        # 
        arglines = []

        # 
        for i, argstruct in enumerate(posargs):
            #
            arg = argstruct['def']

            # 
            argstr = arg.arg
            argstr += ' '*(max_name_len - len(arg.arg))
    
            # 
            if arg.annotation != None:
                argstr += f': {arg.annotation.id}'
            else:
                argstr += ': type'

            #
            arglines.append(argstr)
        
        # 
        for i, kwarg in enumerate(kwargs):

            # 
            argstr = kwarg['def'].arg
            argstr += ' '*(max_name_len - len(kwarg['def'].arg))
    
            # 
            if kwarg["type"] != None:
                ta = kwarg["type"]
                argstr += f': {ta}' + ' '*(max_annotation_len - len(ta))
            else:
                argstr += ' '*(2 + max_annotation_len)

            #
            argstr += f' = {astunparse.unparse(kwarg["default"]).strip()}'

            #
            arglines.append(argstr)
        
        join_str = '\n\t\t'
        arglines = [f"{join_str}{argstr}" for argstr in arglines]
        return '(' + ','.join(arglines) + '\n\t)'

    raise NotImplementedError(posargs, kwargs)

def function_to_argsstr(f: ast.Module) -> str:
    # 
    args          = fm_to_args(f)
    posargs       = args['posargs']
    kwargs        = args['kwargs']
    has_varargs   = bool(f.args.vararg is not None)
    has_varkwargs = bool(f.args.kwarg is not None)
#     print('hmm', f.name, posargs, kwargs)

    # 
    max_name_len       = max(
        [len(argstruct['def'].arg) for argstruct in posargs] + \
        [len(kwarg['def'].arg) for kwarg in kwargs],
        default = 0
    )
    max_annotation_len = max(
        [
            len(posarg['type']) 
            for posarg in posargs
        ] + [
            len(kwarg['type']) 
            for kwarg in kwargs
        ] + [0],
        default = 0
    )
    
    #
    arglines = []

    # 
    for i, argstruct in enumerate(posargs):
        #
        arg = argstruct['def']

        # 
        argstr = arg.arg
        argstr += ' '*(max_name_len - len(arg.arg))

        # 
        if arg.annotation != None:
            # ta = type annotation
            ta      = argstruct['type']
            argstr += f': {ta}'
        else:
            argstr += ': type'

        #
        arglines.append(argstr)
    
    # 
    if has_varargs:
        arglines.append(f"*{astunparse.unparse(f.args.vararg).strip()}")
        
    # 
    for i, kwarg in enumerate(kwargs):

        # 
        argstr = kwarg['def'].arg
        argstr += ' '*(max_name_len - len(kwarg['def'].arg))

        # 
        if kwarg["type"] != None:
            ta = kwarg["type"]
            argstr += f': {ta}' + ' '*(max_annotation_len - len(ta))
        else:
            argstr += ' '*(2 + max_annotation_len)

        #
        argstr += f' = {astunparse.unparse(kwarg["default"]).strip()}'

        #
        arglines.append(argstr)

    # 
    if has_varkwargs:
        arglines.append(f"**{astunparse.unparse(f.args.kwarg).strip()}")
    
    # 
    if len(arglines) == 0:
        return '()'
    if len(arglines) == 1:
        return '(' + arglines[0] + ')'
    if len(arglines) == 2 and has_varargs and has_varkwargs:
        return '(' + ', '.join(arglines) + ')'
    
    # 
    join_str = '\n\t\t'
    arglines = [f"{join_str}{argstr}" for argstr in arglines]
    return '(' + ','.join(arglines) + '\n\t)'

def fm_to_signature(f: ast.Module) -> str:
    global testing

    # 
    signature  = f'def {f.name}'
    signature += function_to_argsstr(f)

    if testing:
        print(signature)

    #
    if f.returns != None:
        signature += f' -> {astunparse.unparse(f.returns).strip()}'
    else:
        signature += f' -> type'

    #
    signature += ':'
    
    return signature

def tree_to_func_modules(tree: ast.Module) -> List[ast.Module]:
    return [
        f
        for f in tree.body
        if isinstance(f, ast.FunctionDef)
    ]

def parse_pyfpath(pyfpath: str) -> str:
    global testing 

    # 
    funcnames = pyfpath_to_funcnames(pyfpath)

    for funcname in funcnames:

        # 
        astm                = pyfpath_funcname_to_astm(pyfpath, funcname)
        signature           = fm_to_signature(astm)
        
        # 
        signature_linerange = pyfpath_funcname_to_signature_linerange(pyfpath, funcname)
        next_line = fpath_linerange_to_str(
            pyfpath,
            signature_linerange['end']+1,
            signature_linerange['end']+1,
        )
        
        # 
        if not next_line.lstrip().startswith("'''") and len(signature.split('\n')) > 1:
            signature += "\n    ''''''"
        
        # 
        if testing == False:
            replace_fpath_linerange(
                signature,
                pyfpath,
                signature_linerange['start'],
                signature_linerange['end'],
            )

def parse_args():
    parser = argparse.ArgumentParser()

    #
    parser.add_argument('--file_path', required=True, type=str)

    #
    args, _ = parser.parse_known_args()
    return vars(args)

if __name__ == "__main__":

    #
    args = parse_args()
    parse_pyfpath(args['file_path'])
