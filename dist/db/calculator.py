#!/usr/bin/env python3
"""Safe arithmetic calculator CLI and library."""

from __future__ import annotations

import argparse
import ast
import math
import operator
import sys
from typing import Any

_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_FUNCTIONS = {
    "abs": abs,
    "acos": math.acos,
    "acosh": math.acosh,
    "asin": math.asin,
    "asinh": math.asinh,
    "atan": math.atan,
    "atan2": math.atan2,
    "atanh": math.atanh,
    "ceil": math.ceil,
    "cos": math.cos,
    "cosh": math.cosh,
    "degrees": math.degrees,
    "erf": math.erf,
    "erfc": math.erfc,
    "exp": math.exp,
    "expm1": math.expm1,
    "fabs": math.fabs,
    "factorial": math.factorial,
    "floor": math.floor,
    "fmod": math.fmod,
    "gamma": math.gamma,
    "hypot": math.hypot,
    "lgamma": math.lgamma,
    "log": math.log,
    "log10": math.log10,
    "log1p": math.log1p,
    "log2": math.log2,
    "max": max,
    "min": min,
    "pow": pow,
    "radians": math.radians,
    "prod": math.prod,
    "round": round,
    "sin": math.sin,
    "sinh": math.sinh,
    "sqrt": math.sqrt,
    "tan": math.tan,
    "tanh": math.tanh,
    "trunc": math.trunc,
}

_ALLOWED_CONSTANTS = {
    "e": math.e,
    "pi": math.pi,
    "tau": math.tau,
}

_MAX_EXPRESSION_LENGTH = 256
_MAX_AST_NODES = 100
_MAX_INTEGER_BITS = 4096
_MAX_ABS_VALUE = 1e100


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_number(value: Any) -> int | float:
    if not _is_number(value):
        raise ValueError("Only numeric values are allowed.")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Result must be finite.")
    if isinstance(value, int) and value.bit_length() > _MAX_INTEGER_BITS:
        raise ValueError("Integer result is too large.")
    if abs(value) > _MAX_ABS_VALUE:
        raise ValueError("Result is too large.")
    return value


class SafeExpressionEvaluator(ast.NodeVisitor):
    def visit_Expression(self, node: ast.Expression) -> Any:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)
        _validate_number(left)
        _validate_number(right)
        op = _ALLOWED_BIN_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}.")
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("Exponent magnitude cannot exceed 1000.")
        return _validate_number(op(left, right))

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self.visit(node.operand)
        _validate_number(operand)
        op = _ALLOWED_UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}.")
        return _validate_number(op(operand))

    def visit_Call(self, node: ast.Call) -> Any:
        if not isinstance(node.func, ast.Name):
            raise ValueError("Function calls must be direct names.")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}.")
        if node.keywords:
            raise ValueError("Keyword arguments are not supported.")
        args = [self.visit(arg) for arg in node.args]
        for arg in args:
            _validate_number(arg)

        if func_name == "factorial" and (
            len(args) != 1
            or not isinstance(args[0], int)
            or not 0 <= args[0] <= 170
        ):
            raise ValueError("factorial accepts one integer from 0 to 170.")
        if func_name == "pow":
            if len(args) != 2:
                raise ValueError("pow accepts exactly two arguments.")
            if abs(args[1]) > 1000:
                raise ValueError("Exponent magnitude cannot exceed 1000.")

        return _validate_number(_ALLOWED_FUNCTIONS[func_name](*args))

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}.")

    def visit_Constant(self, node: ast.Constant) -> Any:
        value = node.value
        if isinstance(value, bool):
            raise ValueError("Boolean values are not allowed.")
        if isinstance(value, (int, float)):
            return value
        raise ValueError(f"Unsupported constant: {value!r}.")

    def visit_Num(self, node: ast.Num) -> Any:
        return self.visit_Constant(node)

    def generic_visit(self, node: ast.AST) -> Any:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}.")


def _normalize_result(value: float | int) -> float | int:
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        return value
    return value


def calculate(expression: str) -> float | int:
    """Evaluate a safe arithmetic expression."""
    if expression is None:
        raise ValueError("Expression cannot be empty.")

    expression = str(expression).strip()
    if not expression:
        raise ValueError("Expression cannot be empty.")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise ValueError(
            f"Expression cannot exceed {_MAX_EXPRESSION_LENGTH} characters."
        )

    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > _MAX_AST_NODES:
        raise ValueError(f"Expression cannot exceed {_MAX_AST_NODES} elements.")
    result = SafeExpressionEvaluator().visit(tree)
    return _normalize_result(_validate_number(result))


evaluate = calculate

__all__ = ["calculate", "evaluate", "format_result", "main"]

def format_result(value: float | int) -> str:
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return format(value, ".15g")
    return str(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate a mathematical expression safely.",
    )
    parser.add_argument(
        "expression",
        nargs="?",
        help="Expression such as '2 + 3 * 4' or 'sqrt(9) + 1'.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    expression = args.expression
    if expression is None:
        try:
            expression = input("expression> ")
        except EOFError:
            print("Error: no expression supplied.", file=sys.stderr)
            return 2

    try:
        result = calculate(expression)
    except (SyntaxError, TypeError, ValueError, OverflowError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
