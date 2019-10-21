from mamba import description, it
from unittest.mock import MagicMock

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.anki.hook_vendor import HookVendor
from crowd_anki.config.config_settings import ConfigSettings

with description(HookVendor):
    with it('should not setup the snapshot hooks when the config setting is false'):
        hook_manager = MagicMock()
        config = ConfigSettings(False)
        config.automated_snapshot = False
        vendor = HookVendor(window=MagicMock(), config=config, hook_manager=hook_manager)

        vendor.setup_snapshot_hooks()

        hook_manager.hook.assert_not_called()

with description(HookVendor):
    with it('should setup the snapshot hooks when the config setting is true'):
        hook_manager = MagicMock()
        config = ConfigSettings(False)
        config.automated_snapshot = True
        vendor = HookVendor(window=MagicMock(), config=config, hook_manager=hook_manager)

        vendor.setup_snapshot_hooks()

        hook_manager.hook.assert_called()
