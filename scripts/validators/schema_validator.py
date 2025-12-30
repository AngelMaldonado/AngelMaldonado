"""
Profile JSON Schema Validator

Validates profile.json against the defined JSON Schema to ensure data integrity
before generation pipelines run.
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, Draft7Validator
from jsonschema.exceptions import SchemaError


def load_json_file(file_path: Path) -> dict:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {file_path}")
        print(f"   {str(e)}")
        sys.exit(1)


def validate_profile(profile_path: str = "profile.json", schema_path: str = "schemas/profile.schema.json") -> bool:
    """
    Validate profile.json against the JSON Schema.

    Args:
        profile_path: Path to profile.json
        schema_path: Path to the JSON Schema file

    Returns:
        True if validation passes, exits with code 1 otherwise
    """
    # Convert to Path objects
    profile_file = Path(profile_path)
    schema_file = Path(schema_path)

    print(f"🔍 Validating {profile_file}...")

    # Load profile data
    profile_data = load_json_file(profile_file)

    # Load schema
    schema = load_json_file(schema_file)

    # Validate schema itself first
    try:
        Draft7Validator.check_schema(schema)
    except SchemaError as e:
        print(f"❌ Error: Invalid JSON Schema")
        print(f"   {str(e)}")
        sys.exit(1)

    # Validate profile against schema
    try:
        validate(instance=profile_data, schema=schema)
        print("✅ Validation passed! profile.json is valid.")
        return True
    except ValidationError as e:
        print("❌ Validation failed!")
        print(f"\nError at: {' -> '.join(str(p) for p in e.absolute_path)}")
        print(f"Message: {e.message}")

        if e.context:
            print("\nDetailed errors:")
            for error in e.context:
                print(f"  • {error.message}")

        sys.exit(1)


def main():
    """CLI entry point for validation."""
    validate_profile()


if __name__ == "__main__":
    main()
