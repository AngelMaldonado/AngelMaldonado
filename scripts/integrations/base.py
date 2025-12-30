"""
Base Integration Class

Provides an abstract base class for all platform integrations.
All integrations must extend this class and implement required methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseIntegration(ABC):
    """
    Abstract base class for all platform integrations.

    Integrations follow the template pattern:
    1. validate_config() - Check if integration is properly configured
    2. execute() - Run the integration action
    """

    def __init__(self, config: Dict[str, Any], profile_data: Dict[str, Any]):
        """
        Initialize integration.

        Args:
            config: Integration-specific configuration from profile.json
            profile_data: Full profile data from profile.json
        """
        self.config = config
        self.profile_data = profile_data
        self.enabled = config.get('enabled', False)

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate integration configuration.

        Returns:
            True if configuration is valid and integration can run

        Example:
            def validate_config(self) -> bool:
                token = os.getenv('PLATFORM_API_TOKEN')
                return token is not None and self.config.get('postOnUpdate', False)
        """
        pass

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Execute the integration action.

        Returns:
            Dictionary with execution results:
            {
                'success': bool,
                'platform': str,
                'message': str,
                'details': Any (optional)
            }

        Example:
            def execute(self) -> Dict[str, Any]:
                if not self.is_enabled() or not self.validate_config():
                    return {
                        'success': False,
                        'platform': 'my-platform',
                        'message': 'Integration disabled or misconfigured'
                    }

                # Do integration work...

                return {
                    'success': True,
                    'platform': 'my-platform',
                    'message': 'Successfully posted update'
                }
        """
        pass

    def is_enabled(self) -> bool:
        """
        Check if integration is enabled.

        Returns:
            True if integration is enabled in config
        """
        return self.enabled

    def get_name(self) -> str:
        """
        Get integration name (defaults to class name).

        Returns:
            Integration name
        """
        return self.__class__.__name__.replace('Integration', '').lower()

    def __repr__(self) -> str:
        """String representation of integration."""
        return f"<{self.__class__.__name__} enabled={self.enabled}>"
