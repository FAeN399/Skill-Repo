#!/usr/bin/env python3
"""
Simple greeting script for the Hello World skill.

This demonstrates how to create executable scripts that can be
included in Claude Skills for deterministic operations.
"""

import argparse
import sys
from datetime import datetime


def generate_greeting(name: str = "World") -> str:
    """
    Generate a friendly greeting message.
    
    Args:
        name: Name to greet (default: "World")
    
    Returns:
        Formatted greeting string
    """
    hour = datetime.now().hour
    
    # Time-based greeting
    if hour < 12:
        time_greeting = "Good morning"
    elif hour < 18:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"
    
    return f"{time_greeting}, {name}! 👋"


def main():
    """Main entry point for the greeting script."""
    parser = argparse.ArgumentParser(
        description="Generate friendly greetings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python greet.py
  python greet.py --name Alice
  python greet.py --name "Bob Smith"
        """
    )
    
    parser.add_argument(
        "--name",
        default="World",
        help="Name to greet (default: World)"
    )
    
    args = parser.parse_args()
    
    # Generate and print greeting
    greeting = generate_greeting(args.name)
    print(greeting)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
