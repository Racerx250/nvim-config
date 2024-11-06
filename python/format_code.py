import argparse 
import ast 
import astunparse
import tokenize
from typing import List
from rich import print

def module_to_comments_newlines(f: ast.Module) -> str:
#     print(f)
    function_tokens   = [t for t in tokens if start_line <= t.start[0] <= end_line or start_line <= t.end[0] <= end_line]
    comments_newlines = [
        t 
        for t in function_tokens 
        if (t.type == 62 and t.string == t.line)
        or (t.type == 61 and t.string.strip() == t.line.strip())
    ]

    # 
    inline_comments = [
        t 
        for t in function_tokens 
        if t.type == 61 and t.string.strip() != t.line.strip()
    ] 
    if len(inline_comments) != 0:
        raise NotImplementedError()


def parse_top_level(tree_body: List[ast.Module]) -> List[ast.Module]:
    
    # 
    for f in tree_body:

        if isinstance(f, ast.Import):
            continue
        if isinstance(f, ast.ImportFrom):
            continue
        if isinstance(f, ast.FunctionDef):
            continue
        if isinstance(f, ast.If) and astunparse.unparse(f.test).strip() == "(__name__ == '__main__')":
            continue

        raise NotImplementedError(type(f))

#     print(module_to_comments_newlines(tree_body))

    return {
        'import'    : [
            f
            for f in tree_body
            if isinstance(f, ast.Import)
        ],
        'import_from': [
            f
            for f in tree_body
            if isinstance(f, ast.ImportFrom)
        ],
        'function'   : [
            f
            for f in tree_body
            if isinstance(f, ast.FunctionDef)
        ],
        'main'       : [
            f
            for f in tree_body
            if isinstance(f, ast.If) and astunparse.unparse(f.test).strip() == "(__name__ == '__main__')"
        ]
    }

def import_to_codestr(f: ast.Module) -> str:
    return astunparse.unparse(f).strip()

def importfrom_to_codestr(f: ast.Module) -> str:
    return astunparse.unparse(f).strip()

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
        print('in tuple')
        outer = annotation.value.id
        inner = ', '.join([
            arg_to_typestr(elem)
            for elem in annotation.slice.elts
        ]) 
#         for elem in annotation.slice.elts:
#             print('asdfasdfasdf', arg_to_typestr(elem))
#         complete = outer + "[" + inner + "]"
        complete = f"{outer}[{inner}]"
        print('all args', outer, inner, complete)
        return complete

    raise NotImplementedError(type(annotation.slice)) 

def arg_to_typestr(f: ast.arg) -> str:

    if not isinstance(f, (ast.arg, ast.Constant, ast.Subscript, ast.Call)):
        raise TypeError(type(f))

    if isinstance(f, ast.Subscript):
        return subscript_to_typestr(f)
    
    if isinstance(f, ast.Constant) and f.value == None:
#         print('found None as a constant')
        return 'None'
    if isinstance(f, ast.Call):
#         print('found call', astunparse.unparse(f))
        return astunparse.unparse(f).strip()
    if isinstance(f.annotation, type(None)):
#         print('found None annotation')
        return 'type'
    if isinstance(f.annotation, ast.Name):
        out = f.annotation.id
#         print('name', out)
        return out
    if isinstance(f.annotation, ast.Subscript):
#         print(dir(annotation))
#         print(annotation.value)
#         print(annotation.value.id)
#         print('slice', annotation.slice)
        print('unparsing subscript', astunparse.unparse(f.annotation.slice))
#         print('dir tuple', dir(annotation.slice))
#         print('elements', annotation.slice.elts)
#         print('unparse first element', astunparse.unparse(annotation.slice.elts[0]))
#         print('first element', annotation.slice.elts[0])
#         print('first element value', annotation.slice.elts[0].value)
#         print('first element value id', annotation.slice.elts[0].value.id)
#         print('first element slice', annotation.slice.elts[0].slice)
#         print('first element slice id', annotation.slice.elts[0].slice.id)
#         print('subscript parse', subscript_to_typestr(f))
         
        out = subscript_to_typestr(f.annotation)
        return out
#         return f.annotation.id

    raise NotImplementedError(type(f.annotation))

def function_to_argsstr(f: ast.Module) -> str:
    # 
    num_posargs = len(f.args.args) - len(f.args.defaults)
    num_kwargs  = len(f.args.defaults)
#     posargs     = [f.args.args[i] for i in range(num_posargs)]

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
            'def'    : f.args.args[num_posargs + i],
            'default': f.args.defaults[i],
            'type'   : arg_to_typestr(f.args.args[num_posargs + i])
        }
        for i in range(num_kwargs)
    ]

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
        print(argdefault)
        argstr  = f"{argname}: {argtype} = {argdefault}"
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
                # ta = type annotation
                ta = kwarg["type"]
                argstr += f': {ta}' + ' '*(max_annotation_len - len(ta))
            else:
#                 argstr += ": type"
#                 argstr += ' '*(2 + max_annotation_len - 6)
                argstr += ' '*(2 + max_annotation_len)

            #
            argstr += f' = {astunparse.unparse(kwarg["default"]).strip()}'

            #
            arglines.append(argstr)
        
        join_str = '\n\t\t'
        arglines = [f"{join_str}{argstr}" for argstr in arglines]
        return '(' + ','.join(arglines) + '\n\t)'

#     print(dir(f))
#     print(f.lineno)
#     print(f.name)
#     print([
#         {
#             'start': b.lineno,
#             'end': b.end_lineno,
#         }
#         for b in f.body
#     ])
    raise NotImplementedError(posargs, kwargs)

def function_to_codestr(f: ast.Module, tokens: List[dict]) -> str:
    # 
    start_line        = f.lineno
#     body_start        = min([b.lineno for b in f.body])
    end_line          = f.end_lineno
    function_tokens   = [t for t in tokens if start_line <= t.start[0] <= end_line or start_line <= t.end[0] <= end_line]
#     print(body_start)

    # 
#     pure_comments = [
#         t 
#         for t in function_tokens 
#         if t.type == 61 and t.string.strip() == t.line.strip()
#     ] 
#     # 
#     pure_newlines = [
#         t 
#         for t in function_tokens 
#         if t.type == 62 and t.string == t.line
#     ] 
    # 
    comments_newlines = [
        t 
        for t in function_tokens 
        if (t.type == 62 and t.string == t.line)
        or (t.type == 61 and t.string.strip() == t.line.strip())
    ]

    # 
#     inline_comments = [
#         t 
#         for t in function_tokens 
#         if t.type == 61 and t.string.strip() != t.line.strip()
#     ] 
#     if len(inline_comments) != 0:
#         raise NotImplementedError(inline_comments)

    # 
    codestr  = f'def {f.name}'
    codestr += function_to_argsstr(f)

    #
    if f.returns != None:
        codestr += f' -> {astunparse.unparse(f.returns).strip()}'
    else:
        codestr += f' -> type'

    #
    codestr += ':'

    #
    if len(codestr.split('\n')) > 1:
        codestr += "\n\t''''''"

    # find code blocks
#     print(codestr)
#     print(dir(f))

    # 
    comment_nl_lines = [token.start[0] for token in comments_newlines]
#     code_lines       = [i for b in f.body for i in range(b.lineno, b.end_lineno+1)]
    code_lines       = [b.lineno for b in f.body]
    if len(set(comment_nl_lines).intersection(code_lines)) != 0:
        raise Exception()

    # 
    body_lines       = sorted(comment_nl_lines + code_lines)
    blocks           = []
    last_l_type      = None
    current_block    = []

    for l in body_lines:

        # 
        l_type   = None
        line_obj = None
        if l in comment_nl_lines:
            l_type   = 'comment_nl'
            line_obj = [token.line for token in comments_newlines if token.start[0] == l][0]
        elif l in code_lines:
            l_type   = 'code'
            line_obj = [b for b in f.body if b.lineno == l or b.end_lineno == l][0]
        else:
            raise Exception()
        
        # 
        if last_l_type == None:
            current_block.append({'type': l_type, 'line_obj': line_obj})
            last_l_type = l_type 
            continue

        # 
#         if l_type == 'code' and isinstance(line_obj, ast.Return):
#             blocks.append(current_block)
#             current_block = []
#             current_block.append({'type': l_type, 'line_obj': line_obj})
#             last_l_type = l_type 
#             continue
        
        # 
        if l_type == 'code' and last_l_type == 'code':
            current_block.append({'type': l_type, 'line_obj': line_obj})
            continue

        # 
        if l_type == 'code' and last_l_type == 'comment_nl':
            current_block.append({'type': l_type, 'line_obj': line_obj})
            last_l_type = l_type 
            continue

        # 
        if l_type == 'comment_nl' and last_l_type == 'code':
            blocks.append(current_block)
            current_block = []
            current_block.append({'type': l_type, 'line_obj': line_obj})
            last_l_type = l_type 
            continue

        # 
        if l_type == 'comment_nl' and last_l_type == 'comment_nl':
            current_block.append({'type': l_type, 'line_obj': line_obj})
            last_l_type = l_type 
            continue

        raise Exception(last_l_type, l_type, l)

    blocks.append(current_block)
    
    # 
    for block in blocks:

        # 
        last_l_type  = None
        codestr     += '\n\n'

        for line in block:
#             print(codestr)

            # 
            if line['type'] == 'code' and isinstance(line['line_obj'], ast.Return) and last_l_type == 'code':
                codestr     += '\n\n'
                codestr     += '\n'.join([f'\t{line}' for line in astunparse.unparse(line['line_obj']).strip().split('\n')])
                last_l_type  = line['type']
                continue
            
            # 
            if line['type'] == 'code' and isinstance(line['line_obj'], ast.Return) and last_l_type == 'comment_nl':
                codestr     += '\n'
                codestr     += '\n'.join([f'\t{line}' for line in astunparse.unparse(line['line_obj']).strip().split('\n')])
                last_l_type  = line['type']
                continue
            
            # 
            if last_l_type == None and line['type'] == 'code':
                codestr     += '\t#\n'
                codestr     += '\n'.join([f'\t{line}' for line in astunparse.unparse(line['line_obj']).strip().split('\n')])
                last_l_type  = line['type']
                continue
    
            # 
            if last_l_type == None and line['type'] == 'comment_nl' and line['line_obj'].strip() == '':
                continue

            # 
            if last_l_type == None and line['type'] == 'comment_nl' and line['line_obj'].strip() != '':
                codestr     += '\t'
                codestr     += line['line_obj'].strip()
                last_l_type  = line['type']
                continue

            # 
            if last_l_type == 'code' and line['type'] == 'comment_nl' and line['line_obj'].strip() != '':
                codestr     += '\t'
                codestr     += line['line_obj'].strip()
                last_l_type  = line['type']
                continue

            # 
            if last_l_type == 'comment_nl' and line['type'] == 'code':
                codestr     += '\n'
                codestr     += '\n'.join([f'\t{line}' for line in astunparse.unparse(line['line_obj']).strip().split('\n')])
                last_l_type  = line['type']
                continue

            # 
            if last_l_type == 'code' and line['type'] == 'code':
                codestr     += '\n'
                codestr     += '\n'.join([f'\t{line}' for line in astunparse.unparse(line['line_obj']).strip().split('\n')])
                last_l_type  = line['type']
                continue

            raise Exception(line, last_l_type)


#     print(start_line, end_line, body_lines, comment_nl_lines)

    # 
#     codestr += '\n'.join([f'\t{line}' for line in astunparse.unparse(f.body).split('\n')])
#     print(astunparse.unparse(f))

#     return codestr
#     raise Exception()
    return codestr

def main_to_codestr(f: ast.Module) -> str:
    main_str = astunparse.unparse(f).strip()
    main_str = main_str.replace("(__name__ == '__main__')", "__name__ == '__main__'")
    return main_str

def tbody_to_codestr(tbody: dict, tokens: List[dict]) -> str:
    # 
    codestr  = ''

    if len(tbody['import']) != 0:
        codestr += '\n'.join([import_to_codestr(f) for f in tbody['import']])
        codestr += '\n'

    if len(tbody['import_from']) != 0:
        codestr += '\n'.join([importfrom_to_codestr(f) for f in tbody['import_from']])
        codestr += '\n'

    if len(tbody['import']) != 0 or len(tbody['import_from']) != 0:
        codestr += '\n'

    if len(tbody['function']) != 0:
        codestr += '\n\n'.join([function_to_codestr(f, tokens) for f in tbody['function']])
        codestr += '\n\n'

    codestr += '\n'.join([main_to_codestr(f) for f in tbody['main']])

    return codestr

def parse_pyfpath(pyfpath: str) -> str:
    # 
    with open(pyfpath, 'rt') as file:
        tree = ast.parse(file.read(), filename=pyfpath)

    #
    with tokenize.open(pyfpath) as f:
        tokens = list(tokenize.generate_tokens(f.readline))
    
    
    # 
    tree_body = tree.body
    tree_body = parse_top_level(tree_body)
    codestr   = tbody_to_codestr(tree_body, tokens)

    # 
    with open(pyfpath, 'w') as f:
        f.write(codestr)

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
