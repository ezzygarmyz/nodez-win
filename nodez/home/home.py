import asyncio
import os
import json

from toga import (
    App,
    Window,
    Box,
    Label,
    Divider,
    ImageView,
    Button,
    Icon
)
from toga.constants import Direction, HIDDEN
from toga.colors import RED, BLACK

from .styles.box import BoxStyle
from .styles.divider import DividerStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle
from .styles.image import ImageStyle

from ..client import RPCRequest, get_btcz_price
from ..commands import ClientCommands
from ..system import SystemOp

from ..cash.send import CashWindow
from ..wallet.receive import WalletWindow
from ..browser.navigator import BrowserWindow


class HomeWindow(Window):
    def __init__(self, app:App):
        super().__init__(
            size=(745, 130),
            position=(0, 5),
            resizable=False,
            on_close=self.close_window
        )
        self.client = RPCRequest(self.app)
        self.commands = ClientCommands(self.app)
        self.system = SystemOp(self.app)
        
        self.cash_button = Button(
            icon=Icon("icones/cash"),
            style=ButtonStyle.menu_button,
            on_press=self.open_cash_window
        )
        self.wallet_button = Button(
            icon=Icon("icones/wallet"),
            style=ButtonStyle.menu_button,
            on_press=self.open_wallet_window
        )
        self.explorer_button = Button(
            icon=Icon("icones/explorer"),
            style=ButtonStyle.menu_button
        )
        self.message_button = Button(
            icon=Icon("icones/message"),
            style=ButtonStyle.menu_button
        )
        self.mining_button = Button(
            icon=Icon("icones/mining"),
            style=ButtonStyle.menu_button
        )
        self.browser_button = Button(
            icon=Icon("icones/browser"),
            style=ButtonStyle.menu_button,
            on_press=self.open_browser_window
        )
        self.divider_menu = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.home_divider_menu
        )
        self.divider_vertical = Divider(
            direction=Direction.VERTICAL
        )
        self.total_balances_txt = Label(
            "Total Balance :",
            style=LabelStyle.home_total_balances_txt
        )
        self.total_balances = Label(
            "_._",
            style=LabelStyle.home_total_balances
        )
        self.transparent_balance_txt = Label(
            "T :",
            style=LabelStyle.home_transparent_balance_txt
        )
        self.transparent_balance = Label(
            "_._",
            style=LabelStyle.home_transparent_balance
        )
        self.private_balance_txt = Label(
            "Z :",
            style=LabelStyle.home_private_balance_txt
        )
        self.private_balance = Label(
            "_._",
            style=LabelStyle.home_private_balance
        )
        self.unconfirmed_txt = Label(
            "",
            style=LabelStyle.home_unconfirmed_txt
        )
        self.unconfirmed_balance = Label(
            "",
            style=LabelStyle.home_unconfirmed_balance
        )
        self.btcz_coin = ImageView(
            "resources/btcz_coin.gif",
            style=ImageStyle.btcz_coin
        )
        self.unconfirmed_loading = ImageView(
            "icones/unconfirmed.gif",
            style=ImageStyle.unconfimed_loading
        )
        self.price_txt = Label(
            "BTCZ Price :",
            style=LabelStyle.home_price_txt
        )
        self.price_value = Label(
            "$_._",
            style=LabelStyle.home_price_value
        )
        self.chain_txt = Label(
            "Chain :",
            style=LabelStyle.home_chain_txt
        )
        self.chain_value = Label(
            "NaN",
            style=LabelStyle.home_chain_value
        )
        self.blocks_txt = Label(
            "Blocks :",
            style=LabelStyle.home_blocks_txt
        )
        self.blocks_value = Label(
            "NaN",
            style=LabelStyle.home_blocks_value
        )
        self.sync_txt = Label(
            "Sync :",
            style=LabelStyle.home_sync_txt
        )
        self.sync_value = Label(
            "NaN",
            style=LabelStyle.home_sync_value
        )
        self.dep_text = Label(
            "Dep :",
            style=LabelStyle.home_dep_txt
        )
        self.dep_value = Label(
            "NaN",
            style=LabelStyle.home_dep_value
        )
        self.buttons_box = Box(
            style=BoxStyle.home_buttons_box
        )
        self.node_box = Box(
            style=BoxStyle.home_node_box
        )
        self.total_balances_box = Box(
            style=BoxStyle.balances_box
        )
        self.transparent_balance_box = Box(
            style=BoxStyle.balances_box
        )
        self.private_balance_box = Box(
            style=BoxStyle.balances_box
        )
        self.unconfirmed_balance_box = Box(
            style=BoxStyle.balances_box
        )
        self.price_box = Box(
            style=BoxStyle.price_box
        )
        self.menu_box = Box(
            style=BoxStyle.home_menu_box
        )
        self.blockchain_info_box = Box(
            style=BoxStyle.home_blockchain_info_box
        )
        self.main_box = Box(
            style=BoxStyle.home_main_box
        )
        self.total_balances_box.add(
            self.total_balances,
            self.btcz_coin
        )
        self.transparent_balance_box.add(
            self.transparent_balance_txt,
            self.transparent_balance
        )
        self.private_balance_box.add(
            self.private_balance_txt,
            self.private_balance
        )
        self.unconfirmed_balance_box.add(
            self.unconfirmed_txt,
            self.unconfirmed_balance
        )
        self.price_box.add(
            self.price_txt,
            self.price_value
        )
        self.node_box.add(
            self.total_balances_txt,
            self.total_balances_box,
            self.transparent_balance_box,
            self.private_balance_box,
            self.unconfirmed_balance_box,
            self.price_box
        )
        self.buttons_box.add(
            self.cash_button,
            self.wallet_button,
            self.explorer_button,
            self.message_button,
            self.mining_button,
            self.browser_button
        )
        self.blockchain_info_box.add(
            self.chain_txt,
            self.chain_value,
            self.blocks_txt,
            self.blocks_value,
            self.sync_txt,
            self.sync_value,
            self.dep_text,
            self.dep_value
        )
        self.menu_box.add(
            self.buttons_box,
            self.divider_menu,
            self.blockchain_info_box
        )
        self.main_box.add(
            self.node_box,
            self.divider_vertical,
            self.menu_box
        )
        
        self.content = self.main_box
        
        self.app.add_background_task(
            self.display_main_window  
        )
        
    async def display_main_window(self, widget):
        self.update_price_task = asyncio.create_task(self.update_price())
        self.update_balance_task = asyncio.create_task(self.update_total_balances())
        self.update_info_task = asyncio.create_task(self.update_blockchain_info())
        await asyncio.sleep(2)
        self.show()
        await asyncio.gather(
            self.update_price_task,
            self.update_balance_task,
            self.update_info_task
        )
        
        
    async def update_total_balances(self):
        while True:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            
            try:
                if os.path.exists(db_path):
                    balances = self.client.z_getTotalBalance()
                    unconfirmed_balances = self.client.getUnconfirmedBalance()
                else:
                    balances = await self.commands.z_getTotalBalance()
                    unconfirmed_balances = self.commands.getUnconfirmedBalance()

                if balances is not None:
                    total = self.format_balance(float(balances.get("total", "NaN")))
                    transparent = self.format_balance(float(balances.get("transparent", "NaN")))
                    private = self.format_balance(float(balances.get("private", "NaN")))
                elif balances is None:
                    total, transparent, private = "NaN", "NaN", "NaN"
                    await asyncio.sleep(1)
                    await self.close_all_windows()

                if unconfirmed_balances is not None and unconfirmed_balances > 0:
                    self.unconfirmed_txt.text = "U :"
                    self.unconfirmed_balance.style.background_color = RED
                    self.unconfirmed_balance.text = f"{unconfirmed_balances}"
                elif unconfirmed_balances is None:
                    self.unconfirmed_txt.text = ""
                    self.unconfirmed_balance.style.background_color = BLACK
                    self.unconfirmed_balance.text = ""

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                self.total_balances.text = f"{total}"
                self.transparent_balance.text = f"{transparent}"
                self.private_balance.text = f"{private}"
                
                await asyncio.sleep(5)
                
            
    async def update_price(self):
        while True:
            price = await get_btcz_price()
            if price is not None:
                price_format = self.format_price(price)
                self.price_value.text = f"${price_format}"
            else:
                self.price_value.text = "$ NaN"
            await asyncio.sleep(600)
            
    
    async def update_blockchain_info(self):
        while True:
            config_path = self.app.paths.config
            db_path = os.path.join(config_path, 'config.db')
            if os.path.exists(db_path):
                info = self.client.getBlockchainInfo()
                if info is not None:
                    chain = info["chain"]
                    blocks = info["blocks"]
                    sync = info["verificationprogress"]
                deprecation = self.client.getDeprecationInfo()
                if deprecation is not None:
                    dep = deprecation["deprecationheight"]
            if not os.path.exists(db_path):
                info = await self.commands.getBlockchainInfo()
                if isinstance(info, str):
                    info = json.loads(info)
                    if info is not None:
                        chain = info.get('chain')
                        blocks = info.get('blocks')
                        sync = info.get('verificationprogress')
                deprecation = await self.commands.getDeprecationInfo()
                if isinstance(deprecation, str):
                    deprecation = json.loads(deprecation)
                    if deprecation is not None:
                        dep = deprecation.get('deprecationheight')
            sync_percentage = sync * 100
            self.chain_value.text = f"{chain}"
            self.blocks_value.text = f"{blocks}"
            self.sync_value.text = f"%{float(sync_percentage):.2f}"
            self.dep_value.text = f"{dep}"
            await asyncio.sleep(5)
            
    
    def open_cash_window(self, button):
        self.cash_button.style.visibility = HIDDEN
        self.cash_window = CashWindow(
            self.app,
            self.cash_button
        )
        self.system.update_settings('cash_window', True)
        
    def open_wallet_window(self, button):
        self.wallet_button.style.visibility = HIDDEN
        self.wallet_window = WalletWindow(
            self.app,
            self.wallet_button
        )
        self.system.update_settings('wallet_window', True)
        
    def open_browser_window(self, button):
        self.browser_button.style.visibility = HIDDEN
        self.browser_window = BrowserWindow(
            self.app,
            self.browser_button
        )
        self.system.update_settings('browser_window', True)
            
            
    async def close_window(self, window):
        if self.system.check_window_is_open():
            return

        async def on_confirm(window, result):
            if result is False:
                return
            if result is True:
                try:
                    tasks = [task for task in (self.update_price_task, self.update_balance_task, self.update_info_task) if not task.done()]
                    for task in tasks:
                        task.cancel()

                    await asyncio.gather(*tasks, return_exceptions=True)
                except asyncio.CancelledError:
                    pass
                self.system.clean_config_path()
                self.close()
                await asyncio.sleep(1)
                self.app.main_window.show()

        self.question_dialog(
            "Exit GUI...",
            "You are about to exit and return to the main wizard, are you sure?",
            on_result=on_confirm
        )
        

    async def close_all_windows(self):
        async def on_confirm(window, result):
            if result is None:
                try:
                    tasks = [task for task in (self.update_price_task, self.update_balance_task, self.update_info_task) if not task.done()]
                    for task in tasks:
                        task.cancel()

                    await asyncio.gather(*tasks, return_exceptions=True)
                except asyncio.CancelledError:
                    pass
                self.system.clean_config_path()
        active_windows = list(self.app.windows)
        for active_window in active_windows:
            if not active_window.title.startswith("Node-Z"):
                active_window.close()
        await asyncio.sleep(1)
        self.app.main_window.show()
        self.error_dialog(
            "Connection Lost",
            "The application has lost connection to the node. Please check your network connection or node status.",
            on_result=on_confirm
        )
                    
    
    def format_balance(self, total):
        formatted_total = '{:.8f}'.format(total)  
        parts = formatted_total.split('.')  
        integer_part = parts[0]
        decimal_part = parts[1] 

        if len(integer_part) > 4:
            digits_to_remove = len(integer_part) - 4
            formatted_decimal = decimal_part[:-digits_to_remove]
        else:
            formatted_decimal = decimal_part

        formatted_balance = integer_part + '.' + formatted_decimal
        return formatted_balance
    
    
    def format_price(self, price):
        if price > 0.00000001 and price < 0.0000001:
            return f"{price:.10f}"
        elif price > 0.0000001 and price < 0.000001:
            return f"{price:.9f}"
        elif price > 0.000001 and price < 0.00001:
            return f"{price:.8f}"
        elif price > 0.00001 and price < 0.0001:
            return f"{price:.7f}"
        elif price > 0.0001 and price < 0.001:
            return f"{price:.6f}"
        elif price > 0.001 and price < 0.01:
            return f"{price:.5f}"
        elif price > 0.01 and price < 0.1:
            return f"{price:.4f}"
        elif price > 0.1 and price < 1:
            return f"{price:.3f}"
        elif price > 1 and price < 10:
            return f"{price:.2f}"
        elif price > 10 and price < 100:
            return f"{price:.1f}"
        else:
            return f"{price:.0f}"