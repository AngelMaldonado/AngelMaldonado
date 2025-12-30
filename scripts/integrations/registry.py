"""
Integration Registry

Central registry for all available platform integrations.
Handles discovery, registration, and execution of integrations.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Type, List, Any
from scripts.integrations.base import BaseIntegration


class IntegrationRegistry:
    """
    Registry for managing all available integrations.

    Integrations are automatically registered and can be executed
    based on profile.json configuration.
    """

    _integrations: Dict[str, Type[BaseIntegration]] = {}

    @classmethod
    def register(cls, name: str, integration_class: Type[BaseIntegration]) -> None:
        """
        Register a new integration.

        Args:
            name: Integration identifier (e.g., 'linkedin', 'twitter')
            integration_class: Integration class extending BaseIntegration
        """
        cls._integrations[name] = integration_class
        print(f"📝 Registered integration: {name}")

    @classmethod
    def get_integration(cls, name: str) -> Type[BaseIntegration]:
        """
        Get integration class by name.

        Args:
            name: Integration identifier

        Returns:
            Integration class or None if not found
        """
        return cls._integrations.get(name)

    @classmethod
    def list_integrations(cls) -> List[str]:
        """
        List all registered integrations.

        Returns:
            List of integration names
        """
        return list(cls._integrations.keys())

    @classmethod
    def run_all(cls, profile_path: str = "profile.json") -> List[Dict[str, Any]]:
        """
        Run all enabled integrations from profile.json.

        Args:
            profile_path: Path to profile.json

        Returns:
            List of execution results from all integrations
        """
        # Load profile data
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Profile file not found: {profile_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {profile_path}")
            print(f"   {str(e)}")
            sys.exit(1)

        integrations_config = profile_data.get('integrations', {})

        if not integrations_config:
            print("ℹ️  No integrations configured in profile.json")
            return []

        results = []
        enabled_count = 0

        print(f"\n🔌 Running Integrations...")
        print(f"   Available: {', '.join(cls.list_integrations())}")

        for name, config in integrations_config.items():
            integration_class = cls.get_integration(name)

            if not integration_class:
                print(f"⚠️  Warning: Integration '{name}' not found (skipping)")
                continue

            integration = integration_class(config, profile_data)

            if not integration.is_enabled():
                print(f"⏭️  Skipping {name}: disabled in config")
                continue

            enabled_count += 1
            print(f"\n▶️  Running {name} integration...")

            try:
                result = integration.execute()
                results.append(result)

                if result.get('success'):
                    print(f"✅ {name}: {result.get('message', 'Success')}")
                else:
                    print(f"⚠️  {name}: {result.get('message', 'Failed')}")

            except Exception as e:
                error_result = {
                    'success': False,
                    'platform': name,
                    'message': f'Error: {str(e)}',
                    'error': str(e)
                }
                results.append(error_result)
                print(f"❌ {name}: {str(e)}")

        if enabled_count == 0:
            print("\nℹ️  No integrations are enabled")
        else:
            success_count = sum(1 for r in results if r.get('success'))
            print(f"\n📊 Integration Results: {success_count}/{enabled_count} successful")

        return results


def load_profile(profile_path: str = "profile.json") -> dict:
    """
    Load profile data from JSON file.

    Args:
        profile_path: Path to profile.json

    Returns:
        Profile data dictionary
    """
    with open(profile_path, 'r', encoding='utf-8') as f:
        return json.load(f)
