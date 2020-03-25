import asyncio

import pytest

from tests.service import ServiceSimultaneous
from throttler import ThrottlerSimultaneous


class TestThrottlerSimultaneous:
    @pytest.mark.parametrize(
        ('max_simultaneous', 'count'), ((1, 10), (3, 10), (100, 500))
    )
    def test_via_service_simultaneous(self, max_simultaneous: int, count: int):
        s = ServiceSimultaneous(max_simultaneous)
        t = ThrottlerSimultaneous(max_simultaneous)

        async def request(value: float):
            async with t:
                return await s.get(value)

        main = asyncio.gather(*[request(v) for v in range(count)])
        asyncio.get_event_loop().run_until_complete(main)
