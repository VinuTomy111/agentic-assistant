import ast
import operator
import logging

# Supported operators for safety
_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def _eval(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        op = _OP_MAP[type(node.op)]
        return op(_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        op = _OP_MAP[type(node.op)]
        return op(_eval(node.operand))
    else:
        raise TypeError(f"Unsupported node type: {type(node)}")

def calculate(expression: str) -> str:
    """
    Evaluate a basic math expression safely.
    """
    logging.info(f"Using tool: calculate with expression: '{expression}'")
    try:
        # replace any common string equivalents just in case
        expression = expression.replace('^', '**')
        # Parse and statically evaluate
        node = ast.parse(expression, mode='eval').body
        result = _eval(node)
        return str(result)
    except Exception as e:
        error_msg = f"Error calculating the expression '{expression}'. Make sure it's valid arithmetic. Error: {str(e)}"
        logging.error(error_msg)
        return error_msg
