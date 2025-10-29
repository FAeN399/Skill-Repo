#!/usr/bin/env python3
"""
Example Generator for Claude Skills

Generates realistic usage examples from Python scripts by introspecting
argument parsers and function signatures.
"""

import argparse
import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional


class ExampleGenerator:
    """Generates usage examples from Python scripts."""

    def __init__(self, script_path: str):
        self.script_path = Path(script_path)

        if not self.script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        with open(self.script_path, 'r') as f:
            self.content = f.read()

        try:
            self.tree = ast.parse(self.content)
        except SyntaxError as e:
            raise ValueError(f"Failed to parse {script_path}: {e}")

    def find_argparse_usage(self) -> Optional[Dict]:
        """Extract argparse configuration from script."""
        argparse_info = {
            'description': None,
            'arguments': []
        }

        for node in ast.walk(self.tree):
            # Find ArgumentParser initialization
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'attr') and node.func.attr == 'ArgumentParser':
                    # Extract description
                    for keyword in node.keywords:
                        if keyword.arg == 'description':
                            if isinstance(keyword.value, ast.Constant):
                                argparse_info['description'] = keyword.value.value

                # Find add_argument calls
                if hasattr(node.func, 'attr') and node.func.attr == 'add_argument':
                    arg_info = self._parse_add_argument(node)
                    if arg_info:
                        argparse_info['arguments'].append(arg_info)

        return argparse_info if argparse_info['arguments'] else None

    def _parse_add_argument(self, node: ast.Call) -> Optional[Dict]:
        """Parse an add_argument() call."""
        arg = {}

        # Get positional argument (the argument name)
        if node.args:
            if isinstance(node.args[0], ast.Constant):
                arg['name'] = node.args[0].value

        # Get keyword arguments
        for keyword in node.keywords:
            if keyword.arg == 'help':
                if isinstance(keyword.value, ast.Constant):
                    arg['help'] = keyword.value.value
            elif keyword.arg == 'default':
                if isinstance(keyword.value, ast.Constant):
                    arg['default'] = keyword.value.value
            elif keyword.arg == 'action':
                if isinstance(keyword.value, ast.Constant):
                    arg['action'] = keyword.value.value
            elif keyword.arg == 'required':
                if isinstance(keyword.value, ast.Constant):
                    arg['required'] = keyword.value.value

        return arg if 'name' in arg else None

    def find_main_function(self) -> Optional[ast.FunctionDef]:
        """Find the main() function if it exists."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'main':
                return node
        return None

    def generate_examples(self, format: str = 'markdown') -> str:
        """Generate usage examples in specified format."""
        examples = []

        # Try to find argparse usage
        argparse_info = self.find_argparse_usage()

        if argparse_info:
            examples.extend(self._generate_argparse_examples(argparse_info))
        else:
            # Fallback: generate basic example
            examples.append({
                'title': 'Basic Usage',
                'command': f'python {self.script_path.name}',
                'description': 'Run the script with default settings'
            })

        if format == 'markdown':
            return self._format_markdown(examples)
        elif format == 'text':
            return self._format_text(examples)
        else:
            raise ValueError(f"Unknown format: {format}")

    def _generate_argparse_examples(self, argparse_info: Dict) -> List[Dict]:
        """Generate examples based on argparse configuration."""
        examples = []
        script_name = self.script_path.name

        # Example 1: Help
        examples.append({
            'title': 'Show Help',
            'command': f'python {script_name} --help',
            'description': 'Display usage information and available options'
        })

        # Example 2: Basic usage (required args only)
        required_args = [arg for arg in argparse_info['arguments']
                        if arg.get('required', False)]

        if required_args:
            cmd_parts = [f'python {script_name}']
            for arg in required_args:
                arg_name = arg['name']
                if arg_name.startswith('--'):
                    cmd_parts.append(f"{arg_name} <value>")
                else:
                    cmd_parts.append(f"<{arg_name}>")

            examples.append({
                'title': 'Basic Usage',
                'command': ' '.join(cmd_parts),
                'description': 'Run with required arguments'
            })

        # Example 3: With optional args
        optional_args = [arg for arg in argparse_info['arguments']
                        if not arg.get('required', False) and
                        arg['name'].startswith('--')]

        if optional_args and len(optional_args) <= 3:
            cmd_parts = [f'python {script_name}']

            # Add required args
            for arg in required_args:
                if arg['name'].startswith('--'):
                    cmd_parts.append(f"{arg['name']} value")
                else:
                    cmd_parts.append("input")

            # Add one optional arg as example
            if optional_args:
                sample_opt = optional_args[0]
                if sample_opt.get('action') == 'store_true':
                    cmd_parts.append(sample_opt['name'])
                else:
                    cmd_parts.append(f"{sample_opt['name']} value")

            examples.append({
                'title': 'Advanced Usage',
                'command': ' '.join(cmd_parts),
                'description': f"Use optional parameters: {', '.join(a['name'] for a in optional_args[:2])}"
            })

        return examples

    def _format_markdown(self, examples: List[Dict]) -> str:
        """Format examples as markdown."""
        output = []
        output.append(f"## Usage Examples for `{self.script_path.name}`\n")

        for i, example in enumerate(examples, 1):
            output.append(f"### {example['title']}\n")
            if 'description' in example:
                output.append(f"{example['description']}\n")
            output.append(f"```bash\n{example['command']}\n```\n")

        return '\n'.join(output)

    def _format_text(self, examples: List[Dict]) -> str:
        """Format examples as plain text."""
        output = []
        output.append(f"Usage Examples for {self.script_path.name}")
        output.append("=" * 60)

        for i, example in enumerate(examples, 1):
            output.append(f"\n{i}. {example['title']}")
            if 'description' in example:
                output.append(f"   {example['description']}")
            output.append(f"   $ {example['command']}")

        output.append("")
        return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate usage examples from Python scripts"
    )
    parser.add_argument(
        'script',
        help="Path to Python script to analyze"
    )
    parser.add_argument(
        '--format',
        choices=['markdown', 'text'],
        default='markdown',
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        '--all-scripts',
        action='store_true',
        help="Generate examples for all scripts in directory (not implemented)"
    )

    args = parser.parse_args()

    try:
        script_path = Path(args.script)

        if script_path.is_dir():
            # If given a skill directory, find scripts
            scripts_dir = script_path / "scripts"
            if scripts_dir.exists():
                scripts = list(scripts_dir.glob("*.py"))
                if not scripts:
                    print("No Python scripts found in scripts/ directory", file=sys.stderr)
                    sys.exit(1)

                for script in scripts:
                    try:
                        generator = ExampleGenerator(str(script))
                        print(generator.generate_examples(args.format))
                        print()  # Blank line between scripts
                    except Exception as e:
                        print(f"Warning: Could not generate examples for {script.name}: {e}",
                              file=sys.stderr)
            else:
                print(f"Error: {script_path} has no scripts/ directory", file=sys.stderr)
                sys.exit(1)
        else:
            # Single script
            generator = ExampleGenerator(args.script)
            print(generator.generate_examples(args.format))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
