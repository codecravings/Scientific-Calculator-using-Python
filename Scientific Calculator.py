

import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox, font as tkfont


# ---------------------------------------------------------------------------
# Safe expression evaluator (replaces dangerous eval())
# ---------------------------------------------------------------------------

class SafeEvaluator:
    """Evaluates mathematical expressions safely using AST parsing."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    FUNCTIONS = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'asinh': math.asinh, 'acosh': math.acosh, 'atanh': math.atanh,
        'log': math.log10, 'ln': math.log, 'log2': math.log2,
        'sqrt': math.sqrt, 'abs': abs, 'factorial': math.factorial,
        'ceil': math.ceil, 'floor': math.floor, 'round': round,
        'degrees': math.degrees, 'radians': math.radians,
    }

    CONSTANTS = {
        'pi': math.pi, 'e': math.e, 'tau': math.tau,
        'inf': math.inf, 'ans': 0,
    }

    def __init__(self):
        self.last_answer = 0

    def evaluate(self, expression):
        self.CONSTANTS['ans'] = self.last_answer
        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError as exc:
            raise ValueError(f"Invalid expression: {exc}") from exc
        result = self._eval_node(tree.body)
        self.last_answer = result
        return result

    def _eval_node(self, node):
        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value!r}")
        if isinstance(node, ast.Name):
            name = node.id
            if name in self.CONSTANTS:
                return self.CONSTANTS[name]
            raise ValueError(f"Unknown name: {name}")
        if isinstance(node, ast.UnaryOp):
            op = self.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op(self._eval_node(node.operand))
        if isinstance(node, ast.BinOp):
            op = self.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return op(left, right)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls are supported")
            func_name = node.func.id
            if func_name not in self.FUNCTIONS:
                raise ValueError(f"Unknown function: {func_name}")
            args = [self._eval_node(arg) for arg in node.args]
            return self.FUNCTIONS[func_name](*args)
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")


# ---------------------------------------------------------------------------
# Color theme
# ---------------------------------------------------------------------------

THEME = {
    'bg':             '#1a1a2e',
    'display_bg':     '#16213e',
    'display_fg':     '#e0e0e0',
    'expr_fg':        '#7f8c8d',
    'number_bg':      '#2d2d44',
    'number_fg':      '#ffffff',
    'number_hover':   '#3d3d5c',
    'operator_bg':    '#e94560',
    'operator_fg':    '#ffffff',
    'operator_hover': '#ff6b81',
    'func_bg':        '#0f3460',
    'func_fg':        '#a8d8ea',
    'func_hover':     '#1a4f8a',
    'equal_bg':       '#e94560',
    'equal_fg':       '#ffffff',
    'equal_hover':    '#ff6b81',
    'memory_bg':      '#533483',
    'memory_fg':      '#d4b8e0',
    'memory_hover':   '#6b44a0',
    'clear_bg':       '#c0392b',
    'clear_fg':       '#ffffff',
    'clear_hover':    '#e74c3c',
    'history_bg':     '#16213e',
    'history_fg':     '#7f8c8d',
    'history_hl':     '#e94560',
    'mode_active':    '#27ae60',
    'mode_inactive':  '#7f8c8d',
    'border':         '#2d2d44',
}


# ---------------------------------------------------------------------------
# Main calculator class
# ---------------------------------------------------------------------------

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.configure(bg=THEME['bg'])
        self.root.minsize(780, 520)
        self.root.geometry("780x520")

        self.evaluator = SafeEvaluator()
        self.degree_mode = True
        self.memory = 0.0
        self.history = []
        self.expression = ""
        self.result_displayed = False
        self.second_mode = False

        self._build_fonts()
        self._build_ui()
        self._bind_keys()

    # --- Fonts ---

    def _build_fonts(self):
        self.font_display = tkfont.Font(family="Consolas", size=28, weight="bold")
        self.font_expr = tkfont.Font(family="Consolas", size=13)
        self.font_btn = tkfont.Font(family="Segoe UI", size=16)
        self.font_btn_sm = tkfont.Font(family="Segoe UI", size=12)
        self.font_func = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.font_history = tkfont.Font(family="Consolas", size=11)

    # --- UI Construction ---

    def _build_ui(self):
        main = tk.Frame(self.root, bg=THEME['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # Left: calculator
        calc_frame = tk.Frame(main, bg=THEME['bg'])
        calc_frame.grid(row=0, column=0, sticky="nsew")
        calc_frame.columnconfigure(0, weight=1)

        self._build_display(calc_frame)
        self._build_buttons(calc_frame)

        # Right: history
        self._build_history(main)

    def _build_display(self, parent):
        disp_frame = tk.Frame(parent, bg=THEME['display_bg'], padx=12, pady=8)
        disp_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=(2, 4))
        parent.rowconfigure(0, weight=0)

        # Status bar (mode + memory indicator)
        status = tk.Frame(disp_frame, bg=THEME['display_bg'])
        status.pack(fill=tk.X)

        self.mode_label = tk.Label(
            status, text="DEG", font=("Segoe UI", 10, "bold"),
            fg=THEME['mode_active'], bg=THEME['display_bg'], anchor="w"
        )
        self.mode_label.pack(side=tk.LEFT)

        self.mem_label = tk.Label(
            status, text="", font=("Segoe UI", 10),
            fg=THEME['memory_fg'], bg=THEME['display_bg'], anchor="w"
        )
        self.mem_label.pack(side=tk.LEFT, padx=(10, 0))

        self.second_label = tk.Label(
            status, text="", font=("Segoe UI", 10, "bold"),
            fg="#e94560", bg=THEME['display_bg'], anchor="e"
        )
        self.second_label.pack(side=tk.RIGHT)

        # Expression line
        self.expr_var = tk.StringVar(value="")
        self.expr_display = tk.Label(
            disp_frame, textvariable=self.expr_var, font=self.font_expr,
            fg=THEME['expr_fg'], bg=THEME['display_bg'], anchor="e"
        )
        self.expr_display.pack(fill=tk.X)

        # Main display
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            disp_frame, textvariable=self.display_var, font=self.font_display,
            fg=THEME['display_fg'], bg=THEME['display_bg'], anchor="e",
            padx=8, pady=4
        )
        self.display.pack(fill=tk.X)

    def _make_btn(self, parent, text, row, col, command, bg, fg, hover,
                  colspan=1, font=None):
        f = font or self.font_btn
        btn = tk.Button(
            parent, text=text, font=f, fg=fg, bg=bg,
            activeforeground=fg, activebackground=hover,
            bd=0, relief=tk.FLAT, command=command, cursor="hand2"
        )
        btn.grid(row=row, column=col, columnspan=colspan,
                 sticky="nsew", padx=1, pady=1)
        btn.bind("<Enter>", lambda e, b=btn, h=hover: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, o=bg: b.configure(bg=o))
        return btn

    def _build_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg=THEME['bg'])
        btn_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        parent.rowconfigure(1, weight=1)

        for c in range(9):
            btn_frame.columnconfigure(c, weight=1)
        for r in range(6):
            btn_frame.rowconfigure(r, weight=1)

        mk = self._make_btn
        F = self.font_func
        S = self.font_btn_sm

        # --- Row 0: Mode + Memory ---
        self.mode_btn = mk(btn_frame, "DEG", 0, 0, self.toggle_mode,
                           THEME['func_bg'], THEME['mode_active'],
                           THEME['func_hover'], font=F)
        mk(btn_frame, "2nd", 0, 1, self.toggle_second,
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "MC", 0, 2, self.mem_clear,
           THEME['memory_bg'], THEME['memory_fg'], THEME['memory_hover'], font=F)
        mk(btn_frame, "MR", 0, 3, self.mem_recall,
           THEME['memory_bg'], THEME['memory_fg'], THEME['memory_hover'], font=F)
        mk(btn_frame, "M+", 0, 4, self.mem_add,
           THEME['memory_bg'], THEME['memory_fg'], THEME['memory_hover'], font=F)
        mk(btn_frame, "M-", 0, 5, self.mem_sub,
           THEME['memory_bg'], THEME['memory_fg'], THEME['memory_hover'], font=F)
        mk(btn_frame, "Ans", 0, 6, lambda: self.insert("ans"),
           THEME['memory_bg'], THEME['memory_fg'], THEME['memory_hover'], font=F)
        mk(btn_frame, "C", 0, 7, self.clear,
           THEME['clear_bg'], THEME['clear_fg'], THEME['clear_hover'], font=F)
        mk(btn_frame, "⌫", 0, 8, self.backspace,
           THEME['clear_bg'], THEME['clear_fg'], THEME['clear_hover'], font=F)

        # --- Row 1: Scientific functions ---
        self.func_buttons_row1 = {}
        self.func_buttons_row1['sin'] = mk(
            btn_frame, "sin", 1, 0, lambda: self.insert_func("sin"),
            THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        self.func_buttons_row1['cos'] = mk(
            btn_frame, "cos", 1, 1, lambda: self.insert_func("cos"),
            THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        self.func_buttons_row1['tan'] = mk(
            btn_frame, "tan", 1, 2, lambda: self.insert_func("tan"),
            THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "x!", 1, 3, lambda: self.apply_unary_func("factorial"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "x\u00b2", 1, 4, lambda: self.insert("**2"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)

        # Numbers 7 8 9 + operators
        for i, d in enumerate(["7", "8", "9"]):
            mk(btn_frame, d, 1, 5 + i, lambda v=d: self.insert(v),
               THEME['number_bg'], THEME['number_fg'], THEME['number_hover'])
        mk(btn_frame, "\u00f7", 1, 8, lambda: self.insert("/"),
           THEME['operator_bg'], THEME['operator_fg'], THEME['operator_hover'])

        # --- Row 2: More functions ---
        self.func_buttons_row2 = {}
        self.func_buttons_row2['asin'] = mk(
            btn_frame, "sin\u207b\u00b9", 2, 0, lambda: self.insert_func("asin"),
            THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        self.func_buttons_row2['acos'] = mk(
            btn_frame, "cos\u207b\u00b9", 2, 1, lambda: self.insert_func("acos"),
            THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        self.func_buttons_row2['atan'] = mk(
            btn_frame, "tan\u207b\u00b9", 2, 2, lambda: self.insert_func("atan"),
            THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "\u221ax", 2, 3, lambda: self.insert_func("sqrt"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "x\u00b3", 2, 4, lambda: self.insert("**3"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)

        for i, d in enumerate(["4", "5", "6"]):
            mk(btn_frame, d, 2, 5 + i, lambda v=d: self.insert(v),
               THEME['number_bg'], THEME['number_fg'], THEME['number_hover'])
        mk(btn_frame, "\u00d7", 2, 8, lambda: self.insert("*"),
           THEME['operator_bg'], THEME['operator_fg'], THEME['operator_hover'])

        # --- Row 3: Logs + constants ---
        mk(btn_frame, "ln", 3, 0, lambda: self.insert_func("ln"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "log", 3, 1, lambda: self.insert_func("log"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "log\u2082", 3, 2, lambda: self.insert_func("log2"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "\u03c0", 3, 3, lambda: self.insert("pi"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "e", 3, 4, lambda: self.insert("e"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)

        for i, d in enumerate(["1", "2", "3"]):
            mk(btn_frame, d, 3, 5 + i, lambda v=d: self.insert(v),
               THEME['number_bg'], THEME['number_fg'], THEME['number_hover'])
        mk(btn_frame, "-", 3, 8, lambda: self.insert("-"),
           THEME['operator_bg'], THEME['operator_fg'], THEME['operator_hover'])

        # --- Row 4: Utilities + 0 ---
        mk(btn_frame, "1/x", 4, 0, lambda: self.apply_unary("1/"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "|x|", 4, 1, lambda: self.insert_func("abs"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "%", 4, 2, lambda: self.insert("%"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "x\u02b8", 4, 3, lambda: self.insert("**"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "\u00b1", 4, 4, self.negate,
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)

        mk(btn_frame, "(", 4, 5, lambda: self.insert("("),
           THEME['number_bg'], THEME['number_fg'], THEME['number_hover'], font=S)
        mk(btn_frame, ")", 4, 6, lambda: self.insert(")"),
           THEME['number_bg'], THEME['number_fg'], THEME['number_hover'], font=S)
        mk(btn_frame, ".", 4, 7, lambda: self.insert("."),
           THEME['number_bg'], THEME['number_fg'], THEME['number_hover'])
        mk(btn_frame, "+", 4, 8, lambda: self.insert("+"),
           THEME['operator_bg'], THEME['operator_fg'], THEME['operator_hover'])

        # --- Row 5: Bottom row ---
        mk(btn_frame, "//", 5, 0, lambda: self.insert("//"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "round", 5, 1, lambda: self.insert_func("round"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "\u230a \u230b", 5, 2, lambda: self.insert_func("floor"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "\u2308 \u2309", 5, 3, lambda: self.insert_func("ceil"),
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)
        mk(btn_frame, "Copy", 5, 4, self.copy_result,
           THEME['func_bg'], THEME['func_fg'], THEME['func_hover'], font=F)

        mk(btn_frame, "0", 5, 5, lambda: self.insert("0"),
           THEME['number_bg'], THEME['number_fg'], THEME['number_hover'],
           colspan=3)
        mk(btn_frame, "=", 5, 8, self.evaluate,
           THEME['equal_bg'], THEME['equal_fg'], THEME['equal_hover'])

    def _build_history(self, parent):
        hist_frame = tk.Frame(parent, bg=THEME['history_bg'], padx=6, pady=6)
        hist_frame.grid(row=0, column=1, sticky="nsew", padx=(4, 2), pady=2)

        header = tk.Frame(hist_frame, bg=THEME['history_bg'])
        header.pack(fill=tk.X)
        tk.Label(
            header, text="History", font=("Segoe UI", 12, "bold"),
            fg=THEME['history_hl'], bg=THEME['history_bg']
        ).pack(side=tk.LEFT)
        tk.Button(
            header, text="Clear", font=("Segoe UI", 9), fg=THEME['history_fg'],
            bg=THEME['history_bg'], bd=0, activeforeground=THEME['history_hl'],
            activebackground=THEME['history_bg'], cursor="hand2",
            command=self.clear_history
        ).pack(side=tk.RIGHT)

        self.history_list = tk.Listbox(
            hist_frame, font=self.font_history, fg=THEME['history_fg'],
            bg=THEME['history_bg'], bd=0, highlightthickness=0,
            selectbackground=THEME['func_bg'], selectforeground=THEME['display_fg'],
            activestyle="none"
        )
        scrollbar = tk.Scrollbar(hist_frame, command=self.history_list.yview)
        self.history_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_list.pack(fill=tk.BOTH, expand=True)
        self.history_list.bind("<Double-1>", self._history_click)

    # --- Keyboard Bindings ---

    def _bind_keys(self):
        self.root.bind("<Return>", lambda e: self.evaluate())
        self.root.bind("<KP_Enter>", lambda e: self.evaluate())
        self.root.bind("<Escape>", lambda e: self.clear())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Delete>", lambda e: self.clear())

        for digit in "0123456789":
            self.root.bind(f"<Key-{digit}>", lambda e, d=digit: self.insert(d))
            self.root.bind(f"<KP_{digit}>", lambda e, d=digit: self.insert(d))

        key_map = {
            'plus': '+', 'minus': '-', 'asterisk': '*', 'slash': '/',
            'period': '.', 'KP_Add': '+', 'KP_Subtract': '-',
            'KP_Multiply': '*', 'KP_Divide': '/', 'KP_Decimal': '.',
            'parenleft': '(', 'parenright': ')', 'percent': '%',
            'asciicircum': '**',
        }
        for key, val in key_map.items():
            self.root.bind(f"<{key}>", lambda e, v=val: self.insert(v))

        self.root.bind("<Control-c>", lambda e: self.copy_result())
        self.root.bind("<Control-v>", lambda e: self._paste())

    # --- Core Logic ---

    def _set_display(self, text):
        self.display_var.set(str(text))

    def _get_expr(self):
        return self.expression

    def insert(self, text):
        if self.result_displayed:
            if text in "0123456789(.":
                self.expression = ""
                self.result_displayed = False
            else:
                self.result_displayed = False
        self.expression += text
        self._set_display(self._format_expression(self.expression))

    def insert_func(self, name):
        if self.result_displayed:
            val = self.expression
            self.expression = f"{name}({val})"
            self.result_displayed = False
        else:
            self.expression += f"{name}("
        self._set_display(self._format_expression(self.expression))

    def apply_unary_func(self, name):
        if self.expression:
            self.expression = f"{name}({self.expression})"
            self._set_display(self._format_expression(self.expression))

    def apply_unary(self, prefix):
        if self.expression:
            self.expression = f"{prefix}({self.expression})"
            self._set_display(self._format_expression(self.expression))

    def negate(self):
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            elif self.expression.startswith("(-"):
                self.expression = self.expression[2:]
                if self.expression.endswith(")"):
                    self.expression = self.expression[:-1]
            else:
                self.expression = f"(-{self.expression})"
            self._set_display(self._format_expression(self.expression))

    def backspace(self):
        if self.result_displayed:
            self.clear()
            return
        if self.expression:
            self.expression = self.expression[:-1]
        if not self.expression:
            self._set_display("0")
        else:
            self._set_display(self._format_expression(self.expression))

    def clear(self):
        self.expression = ""
        self.result_displayed = False
        self._set_display("0")
        self.expr_var.set("")

    def evaluate(self):
        if not self.expression:
            return
        raw_expr = self.expression

        # Handle degree mode: wrap trig args in radians()
        eval_expr = self._prepare_expression(raw_expr)

        try:
            result = self.evaluator.evaluate(eval_expr)
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero")
            return
        except OverflowError:
            messagebox.showerror("Math Error", "Result too large")
            return
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Error", f"Calculation failed: {exc}")
            return

        formatted = self._format_result(result)
        display_expr = self._format_expression(raw_expr)
        self.expr_var.set(f"{display_expr} =")
        self.expression = str(result)
        self._set_display(formatted)
        self.result_displayed = True

        self.history.append((display_expr, formatted))
        self._update_history_list()

    def _prepare_expression(self, expr):
        """Wrap trig function arguments with radians() when in degree mode."""
        if not self.degree_mode:
            return expr

        trig_funcs = ['sin', 'cos', 'tan']
        result = expr

        for func in trig_funcs:
            i = 0
            new_result = ""
            while i < len(result):
                # Check for inverse trig (asin, acos, atan) - skip those
                if i > 0 and result[i-1] == 'a' and result[i:i+len(func)] == func:
                    new_result += result[i:i+len(func)]
                    i += len(func)
                    continue
                # Check if we have the func name and it's not part of another word
                if result[i:i+len(func)] == func:
                    before = result[i-1] if i > 0 else ''
                    if before.isalpha():
                        new_result += result[i]
                        i += 1
                        continue
                    after_idx = i + len(func)
                    if after_idx < len(result) and result[after_idx] == '(':
                        # Find matching paren
                        depth = 0
                        j = after_idx
                        while j < len(result):
                            if result[j] == '(':
                                depth += 1
                            elif result[j] == ')':
                                depth -= 1
                                if depth == 0:
                                    break
                            j += 1
                        inner = result[after_idx+1:j]
                        new_result += f"{func}(radians({inner}))"
                        i = j + 1
                        continue
                new_result += result[i]
                i += 1
            result = new_result

        # For inverse trig in degree mode, wrap result: degrees(asin(...))
        for func in ['asin', 'acos', 'atan']:
            i = 0
            new_result = ""
            while i < len(result):
                if result[i:i+len(func)] == func:
                    before = result[i-1] if i > 0 else ''
                    if before.isalpha():
                        new_result += result[i]
                        i += 1
                        continue
                    after_idx = i + len(func)
                    if after_idx < len(result) and result[after_idx] == '(':
                        depth = 0
                        j = after_idx
                        while j < len(result):
                            if result[j] == '(':
                                depth += 1
                            elif result[j] == ')':
                                depth -= 1
                                if depth == 0:
                                    break
                            j += 1
                        inner = result[after_idx+1:j]
                        new_result += f"degrees({func}({inner}))"
                        i = j + 1
                        continue
                new_result += result[i]
                i += 1
            result = new_result

        return result

    def _format_expression(self, expr):
        """Make the raw expression more readable."""
        replacements = [
            ('**', '^'), ('pi', '\u03c0'), ('sqrt', '\u221a'),
            ('*', '\u00d7'), ('/', '\u00f7'),
        ]
        display = expr
        for old, new in replacements:
            display = display.replace(old, new)
        return display

    def _format_result(self, value):
        if isinstance(value, float):
            if value == float('inf'):
                return "\u221e"
            if value == float('-inf'):
                return "-\u221e"
            if abs(value) > 1e15 or (abs(value) < 1e-10 and value != 0):
                return f"{value:.8e}"
            if value == int(value) and abs(value) < 1e15:
                return str(int(value))
            formatted = f"{value:.10f}".rstrip('0').rstrip('.')
            return formatted
        return str(value)

    # --- Mode Toggles ---

    def toggle_mode(self):
        self.degree_mode = not self.degree_mode
        if self.degree_mode:
            self.mode_label.config(text="DEG", fg=THEME['mode_active'])
            self.mode_btn.config(text="DEG")
        else:
            self.mode_label.config(text="RAD", fg="#3498db")
            self.mode_btn.config(text="RAD")

    def toggle_second(self):
        self.second_mode = not self.second_mode
        if self.second_mode:
            self.second_label.config(text="2nd")
            # Swap trig labels to hyperbolic
            for name, btn in self.func_buttons_row1.items():
                btn.config(text=name + "h")
            for name, btn in self.func_buttons_row2.items():
                btn.config(text=name.replace('a', '') + "h\u207b\u00b9")
            self.func_buttons_row1['sin'].config(
                command=lambda: self.insert_func("sinh"))
            self.func_buttons_row1['cos'].config(
                command=lambda: self.insert_func("cosh"))
            self.func_buttons_row1['tan'].config(
                command=lambda: self.insert_func("tanh"))
            self.func_buttons_row2['asin'].config(
                command=lambda: self.insert_func("asinh"))
            self.func_buttons_row2['acos'].config(
                command=lambda: self.insert_func("acosh"))
            self.func_buttons_row2['atan'].config(
                command=lambda: self.insert_func("atanh"))
        else:
            self.second_label.config(text="")
            self.func_buttons_row1['sin'].config(
                text="sin", command=lambda: self.insert_func("sin"))
            self.func_buttons_row1['cos'].config(
                text="cos", command=lambda: self.insert_func("cos"))
            self.func_buttons_row1['tan'].config(
                text="tan", command=lambda: self.insert_func("tan"))
            self.func_buttons_row2['asin'].config(
                text="sin\u207b\u00b9", command=lambda: self.insert_func("asin"))
            self.func_buttons_row2['acos'].config(
                text="cos\u207b\u00b9", command=lambda: self.insert_func("acos"))
            self.func_buttons_row2['atan'].config(
                text="tan\u207b\u00b9", command=lambda: self.insert_func("atan"))

    # --- Memory Functions ---

    def mem_clear(self):
        self.memory = 0.0
        self.mem_label.config(text="")

    def mem_recall(self):
        self.insert(self._format_result(self.memory))

    def mem_add(self):
        try:
            val = self.evaluator.evaluate(self._prepare_expression(self.expression))
            self.memory += val
            self.mem_label.config(text=f"M={self._format_result(self.memory)}")
        except Exception:
            pass

    def mem_sub(self):
        try:
            val = self.evaluator.evaluate(self._prepare_expression(self.expression))
            self.memory -= val
            self.mem_label.config(text=f"M={self._format_result(self.memory)}")
        except Exception:
            pass

    # --- History ---

    def _update_history_list(self):
        self.history_list.delete(0, tk.END)
        for expr, result in reversed(self.history):
            self.history_list.insert(tk.END, f" {expr}")
            self.history_list.insert(tk.END, f"  = {result}")
            self.history_list.insert(tk.END, "")

    def _history_click(self, event):
        sel = self.history_list.curselection()
        if not sel:
            return
        text = self.history_list.get(sel[0]).strip()
        if text.startswith("= "):
            text = text[2:]
        if text:
            self.expression = text
            self.result_displayed = False
            self._set_display(self._format_expression(text))

    def clear_history(self):
        self.history.clear()
        self.history_list.delete(0, tk.END)

    # --- Clipboard ---

    def copy_result(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.display_var.get())

    def _paste(self):
        try:
            text = self.root.clipboard_get()
            self.insert(text)
        except tk.TclError:
            pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
