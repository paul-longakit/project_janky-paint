"""
Icon resource for JankyPaint.

Provides a simple icon that can be used in the application.
This is designed to be lightweight and not overused.
"""


class IconResource:
    """Minimal icon resource for occasional use in the UI."""

    @staticmethod
    def get_eyedropper_icon() -> str:
        """Return eyedropper tool icon."""
        return "💉"

    @staticmethod
    def get_app_icon() -> str:
        """Return application icon."""
        return "🎨"

    @staticmethod
    def get_brush_icon() -> str:
        """Return brush tool icon."""
        return "🖌"

    @staticmethod
    def get_eraser_icon() -> str:
        """Return eraser tool icon."""
        return "🧼"

    @staticmethod
    def get_bucket_icon() -> str:
        """Return fill bucket tool icon."""
        return "🪣"

    @classmethod
    def get_tool_icon(cls, tool_name: str) -> str:
        """Get icon for a specific tool by name."""
        icon_map = {
            "brush": cls.get_brush_icon(),
            "eraser": cls.get_eraser_icon(),
            "bucket": cls.get_bucket_icon(),
            "eyedropper": cls.get_eyedropper_icon(),
        }
        return icon_map.get(tool_name.lower(), "🔧")
