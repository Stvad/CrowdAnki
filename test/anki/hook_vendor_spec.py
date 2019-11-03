from mamba import description, it
from unittest.mock import MagicMock

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.anki.hook_vendor import HookVendor
from crowd_anki.config.config_settings import ConfigSettings


def setup_vendor(automated_snapshot):
    h = MagicMock()
    config = ConfigSettings()
    config.automated_snapshot = automated_snapshot
    v = HookVendor(window=MagicMock(), config=config, hook_manager=h)

    return v, h


with description(HookVendor):
    with it('should not setup the snapshot hooks when the config setting is false'):
        vendor, hook_manager = setup_vendor(False)

        vendor.setup_snapshot_hooks()

        hook_manager.hook.assert_not_called()

with description(HookVendor):
    with it('should setup the snapshot hooks when the config setting is true'):
        vendor, hook_manager = setup_vendor(True)

        vendor.setup_snapshot_hooks()

        hook_manager.hook.assert_called()
