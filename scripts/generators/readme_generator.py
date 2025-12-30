"""
README Generator

Generates README.md from profile.json using Jinja2 templates with monospace font support.
"""

import json
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from scripts.unicode_utils import to_monospace


def load_profile(profile_path: str = "profile.json") -> dict:
    """Load profile data from JSON file."""
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Profile file not found: {profile_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {profile_path}")
        print(f"   {str(e)}")
        sys.exit(1)


def create_jinja_env(templates_dir: str = "templates/readme") -> Environment:
    """
    Create Jinja2 environment with custom filters.

    Args:
        templates_dir: Directory containing Jinja2 templates

    Returns:
        Configured Jinja2 Environment
    """
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True
    )

    # Add monospace filter
    env.filters['monospace'] = to_monospace

    return env


def generate_readme(
    profile_path: str = "profile.json",
    templates_dir: str = "templates/readme",
    output_path: str = "README.md"
) -> None:
    """
    Generate README.md from profile.json using Jinja2 templates.

    Args:
        profile_path: Path to profile.json
        templates_dir: Directory containing Jinja2 templates
        output_path: Output path for generated README.md
    """
    print(f"📝 Generating README from {profile_path}...")

    # Load profile data
    profile_data = load_profile(profile_path)

    # Check if monospace conversion is enabled
    use_monospace = profile_data.get('metadata', {}).get('style', {}).get('useMonospaceFont', True)

    # Create Jinja2 environment
    env = create_jinja_env(templates_dir)

    # Override monospace filter if disabled in profile
    if not use_monospace:
        env.filters['monospace'] = lambda text: text

    # Load main template
    try:
        template = env.get_template('template.md.jinja2')
    except TemplateNotFound:
        print(f"❌ Error: Template not found: template.md.jinja2")
        print(f"   Expected location: {templates_dir}/template.md.jinja2")
        sys.exit(1)

    # Render template
    try:
        content = template.render(profile=profile_data)
    except Exception as e:
        print(f"❌ Error: Failed to render template")
        print(f"   {str(e)}")
        sys.exit(1)

    # Write to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ README generated successfully: {output_path}")
    except IOError as e:
        print(f"❌ Error: Failed to write {output_path}")
        print(f"   {str(e)}")
        sys.exit(1)


def main():
    """CLI entry point for README generation."""
    generate_readme()


if __name__ == "__main__":
    main()
