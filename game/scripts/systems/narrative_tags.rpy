# game/scripts/systems/narrative_tags.rpy -- C1 Narrative Tag System
# The Embrace of the Twin Angels
# Story: E2.2
# Manages active narrative tags that drive C5 undertow triggers and C2 dialogue pool.

init python:

    class NarrativeTagSystem:
        """C1 Narrative Tag System.

        Tags are registered via set_narrative_tag() in narrative scripts.
        They drive:
          - C5 undertow triggering (e.g. 'identity_shame' -> SHAME_LOOP)
          - C2 angel dialogue pool filtering
        Tags are cleared automatically on scene/chapter switch.
        """

        @staticmethod
        def set_tag(tag):
            """Add a narrative tag to the active set.

            Args:
                tag: Tag string (e.g. 'existence_denied', 'identity_shame').
            """
            global active_narrative_tags
            if not isinstance(active_narrative_tags, set):
                active_narrative_tags = set()
            active_narrative_tags.add(tag)

        @staticmethod
        def has_tag(tag):
            """Check if a tag is currently active.

            Args:
                tag: Tag string to check.

            Returns:
                True if tag is in the active set.
            """
            if not isinstance(active_narrative_tags, set):
                return False
            return tag in active_narrative_tags

        @staticmethod
        def get_active_tags():
            """Return a copy of the current active tag set.

            Returns:
                Set of active tag strings.
            """
            if not isinstance(active_narrative_tags, set):
                return set()
            return set(active_narrative_tags)

        @staticmethod
        def clear_tags():
            """Clear all active narrative tags.

            Called on scene switch and chapter switch.
            """
            global active_narrative_tags
            active_narrative_tags = set()

        @staticmethod
        def remove_tag(tag):
            """Remove a specific tag from the active set.

            Args:
                tag: Tag string to remove.
            """
            global active_narrative_tags
            if isinstance(active_narrative_tags, set):
                active_narrative_tags.discard(tag)


# Global convenience functions for use in narrative scripts
# Usage:
#   $ set_narrative_tag("existence_denied")
#   $ has_tag("existence_denied")
#   $ clear_tags()

python early:
    def set_narrative_tag(tag):
        """Global convenience function to set a narrative tag."""
        NarrativeTagSystem.set_tag(tag)

    def has_narrative_tag(tag):
        """Global convenience function to check a narrative tag."""
        return NarrativeTagSystem.has_tag(tag)

    def clear_tags():
        """Global convenience function to clear all narrative tags."""
        NarrativeTagSystem.clear_tags()

    def get_active_tags():
        """Global convenience function to get active tags."""
        return NarrativeTagSystem.get_active_tags()
