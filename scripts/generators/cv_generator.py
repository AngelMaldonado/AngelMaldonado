"""
CV Generator

Generates LaTeX CV from profile.json using Jinja2 templates.
The generated LaTeX files are then compiled to PDF.
"""

import json
import sys
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


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


def create_latex_jinja_env(templates_dir: str = "templates/cv") -> Environment:
    """
    Create Jinja2 environment configured for LaTeX templates.

    Uses special delimiters to avoid conflicts with LaTeX syntax:
    - Variables: \\VAR{...}
    - Blocks: \\BLOCK{...}
    - Comments: \\#{...}

    Args:
        templates_dir: Directory containing LaTeX templates

    Returns:
        Configured Jinja2 Environment
    """
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        block_start_string='\\BLOCK{',
        block_end_string='}',
        variable_start_string='\\VAR{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        trim_blocks=True,
        autoescape=False,  # LaTeX has its own escaping
        keep_trailing_newline=True
    )

    # Add custom filter for LaTeX escaping if needed
    def latex_escape(text):
        """Escape special LaTeX characters."""
        if not isinstance(text, str):
            return text
        # Basic LaTeX escaping
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    env.filters['latex_escape'] = latex_escape

    return env


def generate_section(env: Environment, section_name: str, profile_data: dict, output_dir: str = "templates/cv/sections") -> None:
    """
    Generate a single LaTeX section from template.

    Args:
        env: Jinja2 environment
        section_name: Name of the section (e.g., 'header', 'experience')
        profile_data: Profile data dictionary
        output_dir: Output directory for generated files
    """
    try:
        template = env.get_template(f'sections/{section_name}.tex.jinja2')
        content = template.render(profile=profile_data)

        output_path = Path(output_dir) / f'{section_name}_generated.tex'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✓ Generated {section_name} section")

    except Exception as e:
        print(f"  ✗ Failed to generate {section_name} section: {str(e)}")
        raise


def compile_pdf(tex_file: str, output_dir: str = "assets/generated") -> bool:
    """
    Compile LaTeX file to PDF using pdflatex.

    Args:
        tex_file: Path to main .tex file
        output_dir: Output directory for PDF

    Returns:
        True if compilation succeeded
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n📄 Compiling LaTeX to PDF...")

    try:
        # Run pdflatex twice for references
        for run in [1, 2]:
            print(f"  Running pdflatex (pass {run}/2)...")
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )

            # LaTeX returns non-zero for warnings, so check PDF existence instead
            pdf_name = Path(tex_file).stem + '.pdf'
            pdf_path = output_path / pdf_name

            if not pdf_path.exists() and result.returncode != 0:
                # Only fail if both: non-zero exit AND no PDF produced
                print(f"❌ pdflatex failed on pass {run}")
                print("Error output:")
                # Show last 1000 chars of output
                print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)
                return False

        # Check if PDF was created
        pdf_name = Path(tex_file).stem + '.pdf'
        pdf_path = output_path / pdf_name

        if pdf_path.exists():
            # Rename to cv.pdf
            final_path = output_path / 'cv.pdf'
            if final_path.exists():
                final_path.unlink()  # Remove old version
            pdf_path.rename(final_path)
            print(f"✅ PDF generated successfully: {final_path}")
            return True
        else:
            print(f"❌ PDF file not found: {pdf_path}")
            return False

    except FileNotFoundError:
        print("❌ Error: pdflatex not found. Please install LaTeX (texlive).")
        print("   On macOS: brew install --cask mactex")
        print("   On Ubuntu: sudo apt-get install texlive-full")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Error: pdflatex timed out")
        return False
    except Exception as e:
        print(f"❌ Error during PDF compilation: {str(e)}")
        return False


def generate_cv(
    profile_path: str = "profile.json",
    templates_dir: str = "templates/cv",
    output_dir: str = "assets/generated"
) -> None:
    """
    Generate CV PDF from profile.json.

    Args:
        profile_path: Path to profile.json
        templates_dir: Directory containing CV templates
        output_dir: Output directory for PDF
    """
    print(f"📝 Generating CV from {profile_path}...")

    # Load profile data
    profile_data = load_profile(profile_path)

    # Create Jinja2 environment
    env = create_latex_jinja_env(templates_dir)

    # Generate all section files
    print("\n📋 Generating LaTeX sections...")
    sections = ['header', 'about', 'experience', 'education', 'skills', 'projects']

    for section in sections:
        generate_section(env, section, profile_data, f'{templates_dir}/sections')

    # Generate main template
    print("\n📄 Generating main CV template...")
    try:
        main_template = env.get_template('modern.tex.jinja2')
        main_content = main_template.render(profile=profile_data)

        main_tex_path = Path(templates_dir) / 'modern_generated.tex'
        with open(main_tex_path, 'w', encoding='utf-8') as f:
            f.write(main_content)

        print(f"  ✓ Generated main template: {main_tex_path}")

        # Compile to PDF
        if compile_pdf(str(main_tex_path), output_dir):
            print(f"\n✅ CV generation complete!")
        else:
            print(f"\n⚠️  LaTeX files generated but PDF compilation failed")
            print(f"   You can manually compile: pdflatex {main_tex_path}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error generating main template: {str(e)}")
        sys.exit(1)


def main():
    """CLI entry point for CV generation."""
    generate_cv()


if __name__ == "__main__":
    main()
