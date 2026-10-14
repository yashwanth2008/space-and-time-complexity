# cpp-complexity

Static time-complexity estimator for C++ code, built on tree-sitter (no compilation/execution needed).

## Setup
```
pip install -r requirements.txt --break-system-packages
```

## Usage
```
python3 main.py path/to/file.cpp --trace
```

## What it currently detects (MVP)
- O(1): no loops/recursion
- O(n): single loop with input-dependent bound
- O(n^k): k nested loops all with input-dependent bounds
- Constant-bound loops (e.g. `for(j=0;j<5;j++)`) are correctly ignored — they don't
  inflate complexity
- O(n): linear recursion (1 recursive call per invocation)
- O(n log n): divide-and-conquer recursion (2+ recursive calls + evidence of halving
  the input, e.g. `/2` or `>>1` anywhere in the function body)
- Anything else with 2+ recursive calls and no detected halving is flagged as
  exponential (rough upper bound, not precise)

## Known limitations (roadmap)
- No STL container complexity lookup table yet (map::find, sort(), etc.)
- No space-complexity analysis yet
- Recursion detection doesn't yet solve general recurrence relations (Master Theorem)
- No handling of loops whose bound is set via a function call (e.g. `i < arr.size()`)
  beyond generic "has identifier -> dependent" heuristic
- Single-file analysis only — no cross-function call graph resolution yet
  (if foo() calls bar() which has a loop, that cost isn't currently propagated into foo())

## Architecture
```
C++ source --> tree-sitter parse --> AST walk --> rule-based classifier --> Big-O + trace
```

See `analyzer.py` for the core logic (`ComplexityAnalyzer` class) and `main.py` for the CLI.



## Still under development
