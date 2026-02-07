# 🧮 Scientific Calculator

A fully-featured scientific calculator built with Python & Tkinter — sleek dark UI, safe expression parsing, and all the math you could want.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 🔢 Core Math
- ➕ ➖ ✖️ ➗ Basic arithmetic with full operator precedence
- 🔁 Parentheses `( )` for complex expressions
- 📐 Modulo `%` and floor division `//`
- 🔋 Power `x^y`, square `x²`, cube `x³`

### 📐 Trigonometry
- 🌊 **Standard:** sin, cos, tan
- 🔄 **Inverse:** sin⁻¹, cos⁻¹, tan⁻¹
- 〰️ **Hyperbolic:** sinh, cosh, tanh (via 2nd mode)
- 🔃 **Inverse Hyperbolic:** asinh, acosh, atanh (via 2nd mode)
- 🔀 **DEG / RAD** toggle — switch angle modes on the fly

### 📊 Advanced Functions
- 📈 Logarithms: `ln`, `log₁₀`, `log₂`
- ❗ Factorial `x!`
- √ Square root `√x`
- 🎯 Absolute value `|x|`
- ⬆️ Ceiling `⌈x⌉` and ⬇️ Floor `⌊x⌋`
- 🔄 Round
- 🔃 Reciprocal `1/x`
- ➕➖ Negate `±`

### 🧠 Constants
- 🥧 **π** (pi) — 3.14159265...
- 📧 **e** (Euler's number) — 2.71828182...
- 🔁 **τ** (tau) — 6.28318530...

### 💾 Memory
- **M+** — Add to memory
- **M-** — Subtract from memory
- **MR** — Recall memory
- **MC** — Clear memory
- 📊 Live memory indicator in status bar

### 📜 History
- 🕐 Full calculation history panel on the right
- 🖱️ Double-click any entry to reuse it
- 🗑️ Clear history button
- 🔄 **Ans** button to recall last answer

### ⌨️ Keyboard Support
| Key | Action |
|-----|--------|
| `0-9` | Number input |
| `+ - * /` | Operators |
| `.` | Decimal point |
| `( )` | Parentheses |
| `^` | Power |
| `%` | Modulo |
| `Enter` | Evaluate `=` |
| `Backspace` | Delete last character |
| `Escape` / `Delete` | Clear all |
| `Ctrl+C` | 📋 Copy result |
| `Ctrl+V` | 📋 Paste from clipboard |
| Numpad | ✅ Full numpad support |

### 🎨 UI
- 🌙 Modern dark theme with color-coded button groups
- 🖲️ Hover effects on every button
- 📏 Expression preview line — see what you're building
- 🔢 Smart result formatting (strips trailing zeros, scientific notation for huge/tiny numbers, ∞ symbol)
- 📐 Resizable window
- 🏷️ Status bar: DEG/RAD mode • Memory value • 2nd mode indicator

### 🔒 Security
- 🛡️ **No `eval()`** — uses a custom AST-based expression parser
- 🚫 Blocks code injection, arbitrary imports, and system calls
- ✅ Only whitelisted math functions and constants are allowed

---

## 🚀 Getting Started

### 📋 Prerequisites

- 🐍 Python 3.8 or higher
- 📦 Tkinter (included with most Python installations)

### ▶️ Run It

```bash
python "Scientific Calculator.py"
```

That's it — no dependencies to install! 🎉

---

## 🖼️ Layout

```
┌──────────────────────────────────────────────┬─────────────┐
│  DEG  M=42                              2nd  │  📜 History  │
│                                    sin(45) = │             │
│                                  0.70710678  │  sin(45)    │
├──────────────────────────────────────────────┤  = 0.707... │
│ DEG │ 2nd │ MC │ MR │ M+ │ M- │Ans│  C │ ⌫  │             │
│ sin │ cos │ tan│ x! │ x² │  7 │ 8 │  9 │  ÷ │  2+3        │
│sin⁻¹│cos⁻¹│tan⁻¹│ √x │ x³ │  4 │ 5 │  6 │  × │  = 5       │
│ ln  │ log │log₂│  π │  e │  1 │ 2 │  3 │  - │             │
│ 1/x │ |x| │  % │ xʸ │  ± │  ( │ ) │  . │  + │             │
│ //  │round│ ⌊⌋ │ ⌈⌉ │Copy│    0    │  = │             │
└──────────────────────────────────────────────┴─────────────┘
```

---

## 🧪 Button Groups

| Color | Group | Examples |
|-------|-------|---------|
| 🔴 Red | Operators & Equals | `+ - × ÷ =` |
| 🔵 Blue | Scientific Functions | `sin cos log √x` |
| 🟣 Purple | Memory | `MC MR M+ M-` |
| 🔴 Dark Red | Clear / Delete | `C ⌫` |
| ⚫ Dark Gray | Numbers & Utilities | `0-9 . ( )` |

---

## 🏗️ Architecture

```
Scientific Calculator.py
├── 🛡️ SafeEvaluator        — AST-based safe math expression parser
├── 🎨 THEME                 — Color palette dictionary
└── 🧮 ScientificCalculator  — Main application class
    ├── _build_fonts()       — Font definitions
    ├── _build_ui()          — Window layout
    ├── _build_display()     — Display + status bar
    ├── _build_buttons()     — Button grid (factory pattern)
    ├── _build_history()     — History panel
    ├── _bind_keys()         — Keyboard shortcuts
    ├── evaluate()           — Expression evaluation pipeline
    ├── _prepare_expression()— DEG/RAD trig wrapping
    ├── _format_result()     — Smart number formatting
    ├── toggle_mode()        — DEG ↔ RAD
    ├── toggle_second()      — Standard ↔ Hyperbolic trig
    ├── mem_*()              — Memory operations
    └── copy/paste           — Clipboard integration
```

---



> 🧮 *Math is not about numbers, equations, computations, or algorithms: it is about understanding.* — William Paul Thurston
