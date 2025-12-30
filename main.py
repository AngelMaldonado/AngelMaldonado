"""
Profile as Code - Main CLI

Orchestrates the automation pipeline for generating README, CV, and running integrations.
"""

import sys
from scripts.validators.schema_validator import validate_profile
from scripts.generators.readme_generator import generate_readme
from scripts.generators.cv_generator import generate_cv

# Import integrations to auto-register them
import scripts.integrations.linkedin  # noqa: F401
from scripts.integrations.registry import IntegrationRegistry


def print_usage():
    """Print CLI usage information."""
    print("Profile as Code - Automation CLI")
    print("\nUsage: uv run main.py <command>")
    print("\nCommands:")
    print("  validate           Validate profile.json against JSON Schema")
    print("  generate-readme    Generate README.md from profile.json")
    print("  generate-cv        Generate CV PDF from profile.json")
    print("  run-integrations   Run platform integrations (LinkedIn, etc.)")
    print("\nExample:")
    print("  uv run main.py validate")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "validate":
        validate_profile()
    elif command == "generate-readme":
        generate_readme()
    elif command == "generate-cv":
        generate_cv()
    elif command == "run-integrations":
        IntegrationRegistry.run_all()
    elif command in ["-h", "--help", "help"]:
        print_usage()
    else:
        print(f"❌ Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
