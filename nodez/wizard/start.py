import asyncio
import os
import subprocess

from toga import (
    App,
    Window,
    Box,
    Label,
    Divider,
    ImageView
)
from toga.constants import Direction
from toga.colors import RED

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle

from ..client import ClientCommands
from ..home.home import MainMenu


class StartNode(Window):
    def __init__(self, app:App, rpc_button, local_button):
        super().__init__(
            title="Loading...",
            size=(280, 90),
            position=(220, 250),
            resizable=False,
            minimizable=False,
            closable=False
        )
        self.command = ClientCommands(self.app)
        self.rpc_button = rpc_button
        self.local_button = local_button
        
        self.starting_txt = Label(
            "Starting Node...",
            style=LabelStyle.starting_txt
        )
        self.divider_top = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.start_divider_top
        )
        self.main_box = Box(
            style=BoxStyle.start_main_box
        )
        self.bitcoinz_coin = ImageView(
            ("resources/btcz_coin1.gif")
        )
        self.main_box.add(
            self.starting_txt,
            self.divider_top,
            self.bitcoinz_coin
        )
        self.content = self.main_box
        self.app.add_background_task(
            self.display_window
        )
        
    async def display_window(self, widget):
        self.local_button.enabled = False
        self.rpc_button.enabled = False
        self.show()
        await self.start_node()
    
    
    async def start_node(self):
        data_path = self.app.paths.data
        bitcoinzd_file = os.path.join(data_path, "bitcoinzd.exe")
        await asyncio.sleep(1)
        await asyncio.create_subprocess_exec(
            bitcoinzd_file,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        await self.check_node_status()
        
        
    async def check_node_status(self):
        await asyncio.sleep(1)
        while True:
            result = await self.command.getInfo()
            if result:
                self.starting_txt.text = "Starting GUI..."
                await asyncio.sleep(1)
                self.close()
                self.app.main_window.hide()
                await asyncio.sleep(2)
                self.app.main_window.content.clear()
                self.app.main_window.content = MainMenu(self.app)
                return
            else:
                self.starting_txt.text = "Loading blocks..."
                print(False)

            await asyncio.sleep(4)