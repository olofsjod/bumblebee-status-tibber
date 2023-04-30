"""Displays the current electricity price with the Tibber API.

Requires the following library:
   * pyTibber

Parameters:
   * tibber.access_token:  Access token which you can get from developer.tibber.com.

contributed by `olofsjod <https://github.com/olofsjod>`
"""

import tibber.const
import tibber
import asyncio

import core.module
import core.widget

class Module(core.module.Module):
    @core.decorators.every(minutes=1, seconds=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.__access_token = self.parameter("access_token", tibber.const.DEMO_TOKEN)

    def full_text(self, widgets):
        tibber_connection = tibber.Tibber(self.__access_token, user_agent="tibber.py")

        async def home_data():
            home = tibber_connection.get_homes()[0]
            await home.fetch_consumption_data()
            await home.update_info()

            await home.update_price_info()
            return home

        async def start():
            await tibber_connection.update_info()
            #print(tibber_connection.name)
            home = await home_data()
            await tibber_connection.close_connection()
            return home

        loop = asyncio.get_event_loop()
        home = loop.run_until_complete(start())

        price_info = home.current_price_info
        return f"{price_info['total']} SEK/kWh"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
