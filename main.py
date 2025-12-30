"""
Profile as Code - Main CLI

Orchestrates the automation pipeline for generating README, CV, and running integrations.
"""

import sys
from scripts.validators.schema_validator import validate_profile
from scripts.generators.readme_generator import generate_readme


def print_usage():
    """Print CLI usage information."""
    print("Profile as Code - Automation CLI")
    print("\nUsage: uv run main.py <command>")
    print("\nCommands:")
    print("  validate           Validate profile.json against JSON Schema")
    print("  generate-readme    Generate README.md from profile.json")
    print("  generate-cv        Generate CV PDF from profile.json (TODO)")
    print("  run-integrations   Run platform integrations (TODO)")
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
        print("❌ Error: generate-cv not yet implemented")
        print("   This command will be added in Phase 4")
        sys.exit(1)
    elif command == "run-integrations":
        print("❌ Error: run-integrations not yet implemented")
        print("   This command will be added in Phase 5")
        sys.exit(1)
    elif command in ["-h", "--help", "help"]:
        print_usage()
    else:
        print(f"❌ Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
