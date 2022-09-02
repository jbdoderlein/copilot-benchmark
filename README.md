# Copilot Benchmark

Platform to test the completions of Github Copilot and Codex.

## Installation

### Installation of a virtualenv

``bash
python -m venv
source venv/bin/activate
```

### Copilot and dependencies installation

``bash
pip install -r requirements.txt
pip install -e .
```

To activate copilot you need to install the copilot plugin on neovim and connect to github with it.

## Usage

The generation and test scripts are available in the `humaneval` and `leetcode` folder.
To get the generation parameters, use the `--help` flag.

The notebook `results.ipynb` allows to visualize and use the test results. The raw results are available in the `humaneval` and `leetcode` folder under the name `results.json`.

The `copilot` folder contains the package to use copilot.

The `utils` folder contains useful functions for code generation and testing.
