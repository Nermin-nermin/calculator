import ast, operator, math, sys, readline

operators = {
    ast.Add : operator.add,
    ast.Sub : operator.sub,
    ast.Mult : operator.mul,
    ast.Div : operator.truediv, 
    ast.FloorDiv : operator.floordiv,
    ast.Pow : operator.pow, 
    ast.Mod : operator.mod, 
    ast.USub : operator.neg, 
    ast.UAdd : operator.pos

}

ENV = {
    'pi' : math.pi, 
    'e' : math.e,
    'tau' : math.tau,
    'sqrt' : math.sqrt,
    'sin' : math.sin,
    'cos' : math.cos,
    'tan' : math.tan, 
    'asin' : math.asin,
    'acos' : math.acos,
    'atan' : math.atan,
    'log' : math.log, 
    'log10' : math.log10,
    'exp' : math.exp,
    'abs' : abs,
    'round' : round
    }

class SafeEval(ast.NodeVisitor):

    def __init__(self, env):
        self.env = env

    def visit_Module(self, node):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError('Only single ecpressions are allowed')
        return self.visit(node.body[0].value)
    
    def visit_Expr(self, node):
        return self.visit(node.value)
    
    def visit_Name(self, node):
        if node.id in self.env:
            return self.visit(node.id)
        raise NameError('UNknown')
    
    def visit_Num(self, node):
        return node.n
    
    def visit_Constant(self, node):
        if isinstance(node.value, (float, int)):
            return node.value
        raise TypeError('Only numbers')

    def visit_UnaryOp(self, node):
        op = operators.get(type(node.op))
        if not op: raise TypeError('Unsupported unary')
        return op(self.visit(node.operand))
    
    def visit_BinOp(self, node):
        op = operators.get(type(node.op))
        if not op: raise TypeError('Unsupported binary')
        left = self.visit(node.left)
        right = self.visit(node.right)
        return op(left, right)
    
    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise TypeError("Unsuported function call")
        name = node.func.id
        fn = self.env.get(name)
        if not callable(fn):
            raise NameError('Unknown function')
        args = [self.visit(a) for a in node.args]
        if node.keywords:
            raise TypeError('Keyword arguments are not supported')
        return fn(*args)
    
    def generic_visit(self, node):
        raise TypeError(f'Unsupported type {type(node).__name__}')
    
  def eval_expr(expr, env):
    tree = ast.parse(expr, mode = 'exec')
    return SafeEval(env).visit(tree)

def run_repl():
    print('Basic Calculator. Type "exit" to quit.')
    env = dict(ENV)
    env['ans'] = 0.0
    while True:
        try:
            line = input('>').strip()
            if line.lower() in {'exit'}:
                break
            if not line:
                continue
            result = eval_expr(line, env)
            env['ans'] = result
            print(result)
        except (KeyboardInterrupt, EOFError):
            print()
            break
        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)

def run_once(expr):
    env = dict(ENV)
    env['ans'] = 0.0
    try:
        print(eval_expr(expr, env))
    except Exception as e:
        print(f'Error: {e}', file = sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_once(''.join(sys.argv[1:]))
    else:
        run_repl()
