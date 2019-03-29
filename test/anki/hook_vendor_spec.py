from mamba import description, it
from unittest.mock import MagicMock

from test_utils.anki import mock_anki_modules

mock_anki_modules()

from crowd_anki.anki.hook_vendor import HookVendor
from crowd_anki.utils.config import AUTOMATED_SNAPSHOT

with description(HookVendor):
    with it('should only setup snapshot hooks if plugin config says so'):
        hook_manager = MagicMock()
        vendor = HookVendor(MagicMock(), hook_manager)
        vendor.config = {AUTOMATED_SNAPSHOT: False}

        vendor.setup_snapshot_hooks()

        hook_manager.hook.assert_not_called()
