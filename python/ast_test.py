import ast

print(ast.dump(ast.parse("""\
@decorator1
@decorator2
def f(a: 'annotation', b=1, c=2, *d, e, f=3, **g) -> 'return annotation':
    pass
"""), indent=4))
