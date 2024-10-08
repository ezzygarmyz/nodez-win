
import os
import json
import asyncio
from datetime import datetime

import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Clipboard

from toga import (
    App,
    Window,
    Box,
    ImageView,
    Button,
    Label,
    Selection,
    Icon,
    OptionContainer,
    OptionItem,
    TextInput,
    PasswordInput,
    Switch,
    Divider
)
from toga.colors import YELLOW, CYAN
from toga.constants import VISIBLE, Direction

from .styles.box import BoxStyle
from .styles.image import ImageStyle
from .styles.label import LabelStyle
from .styles.button import ButtonStyle
from .styles.selection import SelectionStyle
from .styles.container import ContainerStyle
from .styles.input import InputStyle
from .styles.switch import SwitchStyle

from .manage import AddressInfo
from .txids_list import AllTransactions

from ..system import SystemOp
from ..command import ClientCommands
from ..client import RPCRequest



class WalletWindow(Window):
    def __init__(self, app:App, window_button, explorer_button):
        super().__init__(
            title="Wallet Manage",
            size=(800, 700),
            resizable=False,
            minimizable=False,
            on_close=self.close_window
        )
        self.system = SystemOp(self.app)
        self.client = RPCRequest(self.app)
        self.command = ClientCommands(self.app)
        position_center = self.system.windows_screen_center(self.size)
        self.position = position_center
        self.window_button = window_button
        self.explorer_button = explorer_button

        config_path = self.app.paths.config
        self.db_path = os.path.join(config_path, 'config.db')

        self.bitcoinz_coin = ImageView(
            ("resources/btcz_coin1.gif"),
            style=ImageStyle.bitcoinz_coin
        )
        self.transparent_button = Button(
            "Transparent",
            enabled=True,
            style=ButtonStyle.transparent_button,
            on_press=self.switch_to_transparent
        )
        self.shielded_button = Button(
            "Shielded",
            enabled=True,
            style=ButtonStyle.shielded_button,
            on_press=self.switch_to_shielded
        )
        self.transparent_icon = ImageView(
            "icons/transparent_txt.png",
            style=ImageStyle.transparent_icon
        )
        self.shielded_icon = ImageView(
            "icons/shielded_txt.png",
            style=ImageStyle.shielded_icon
        )
        self.switch_button_box = Box(
            style=BoxStyle.switch_button_box
        )
        self.view_key_button = Button(
            icon=Icon("icons/view_key"),
            style=ButtonStyle.wallet_manage_buttons,
            enabled=True,
            on_press=self.display_private_key
        )
        self.import_key_button = Button(
            icon=Icon("icons/import_key"),
            style=ButtonStyle.wallet_manage_buttons,
            enabled=True,
            on_press=self.display_import_window
        )
        self.import_wallet_button = Button(
            icon=Icon("icons/import_wallet"),
            style=ButtonStyle.wallet_manage_buttons,
            enabled=True,
            on_press=self.import_wallet_file
        )
        self.new_address_button = Button(
            icon=Icon("icons/new_addr"),
            enabled=True,
            style=ButtonStyle.wallet_manage_buttons,
            on_press=self.generate_new_address
        )
        self.buttons_box = Box(
            style=BoxStyle.buttons_box
        )
        self.select_address_txt = Label(
            "Addresses :",
            style=LabelStyle.select_address_txt
        )
        self.select_address = Selection(
            accessor="select_address",
            enabled=True,
            style=SelectionStyle.select_address,
            on_change=self.display_address_info
        )
        self.select_address_box = Box(
            style=BoxStyle.select_address_box
        )
        self.address_manage_box = Box(
            style=BoxStyle.address_manage_box
        )
        self.wallet_manage_box = Box(
            style=BoxStyle.wallet_manage_box
        )
        self.merge_info_txt = Label(
            "Merge multiple UTXOs into a single UTXO or note.",
            style=LabelStyle.merge_info_txt
        )
        self.operation_status_txt = Label(
            "- Operation Result -",
            style=LabelStyle.operation_status_txt
        )
        self.remaining_utxos = Label(
            "remainingUTXOs :",
            style=LabelStyle.status_txt
        )
        self.remaining_value = Label(
            "remainingValue :",
            style=LabelStyle.status_txt
        )
        self.merging_utxos = Label(
            "mergingUTXOs :",
            style=LabelStyle.status_txt
        )
        self.merging_value = Label(
            "mergingValue :",
            style=LabelStyle.status_txt
        )
        self.operation_id = Label(
            "OperationID :",
            style=LabelStyle.status_txt
        )
        self.operation_id_output = TextInput(
            readonly=True,
            style=InputStyle.operation_id_output
        )
        self.merge_select_address_txt = Label(
            "Merge to :",
            style=LabelStyle.merge_select_address_txt
        )
        self.merge_select_address = Selection(
            accessor="merge_select_address",
            enabled=True,
            style=SelectionStyle.merge_select_address
        )
        self.merge_list_txt = Label(
            "",
            style=LabelStyle.merge_list_txt
        )
        self.merge_fee_txt = Label(
            "Txfee :",
            style=LabelStyle.merge_fee_txt
        )
        self.merge_fee_input = TextInput(
            placeholder="default 0.0001",
            style=InputStyle.merge_fee_input
        )
        self.scan_button = Button(
            icon=Icon("icons/scan_utxos"),
            enabled= True,
            style=ButtonStyle.scan_button,
            on_press=self.scan_utxos
        )
        self.cancel_button = Button(
            "Cancel",
            enabled=True,
            style=ButtonStyle.cancel_button,
            on_press=self.cancel_merge_utxos
        )
        self.merge_button = Button(
            "Merge",
            enabled=True,
            style=ButtonStyle.merge_button,
            on_press=self.verify_merge_inputs
        )
        self.merge_divider = Divider(
            direction=Direction.VERTICAL
        )
        self.merge_fee_box = Box(
            style=BoxStyle.merge_fee_box
        )
        self.merge_buttons_box = Box(
            style=BoxStyle.merge_buttons_box
        )
        self.merge_address_box = Box(
            style=BoxStyle.select_address_box
        )
        self.merge_reslut_box = Box(
            style=BoxStyle.merge_result_box
        )
        self.merge_operation_box = Box(
            style=BoxStyle.merge_operation_box
        )
        self.merge_manage_box = Box(
            style=BoxStyle.merge_manage_box
        )
        self.wallet_main_box = Box(
            style=BoxStyle.wallet_main_box
        )
        self.wallet_manage_option = OptionItem(
            text="Address Manage",
            enabled=True,
            content=self.wallet_main_box
        )
        self.transactions_list_option = OptionItem(
            text="Transactions List",
            enabled=True,
            content=AllTransactions(
                self.app,
                self.explorer_button
            )
        )
        self.wallet_container = OptionContainer(
            content=[
                self.wallet_manage_option,
                self.transactions_list_option
            ],
            style=ContainerStyle.wallet_container
        )

        self.content = self.wallet_container
        
        self.app.add_background_task(
            self.get_addresses_list
        )



    async def get_addresses_list(self, widget):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.items = transparent_address
        self.merge_select_address.items = transparent_address

        await self.display_window()


    async def display_window(self):
        self.switch_button_box.add(
            self.transparent_icon,
            self.shielded_button
        )
        self.buttons_box.add(
            self.view_key_button,
            self.import_key_button,
            self.import_wallet_button,
            self.new_address_button
        )
        self.select_address_box.add(
            self.select_address_txt,
            self.select_address
        )
        self.wallet_manage_box.add(
            self.switch_button_box,
            self.buttons_box,
            self.select_address_box,
            self.address_manage_box
        )
        self.merge_address_box.add(
            self.merge_select_address_txt,
            self.merge_select_address
        )
        self.merge_operation_box.add(
            self.merge_info_txt,
            self.scan_button
        )
        self.merge_reslut_box.add(
            self.operation_status_txt,
            self.remaining_utxos,
            self.remaining_value,
            self.merging_utxos,
            self.merging_value,
            self.operation_id,
            self.operation_id_output
        )
        self.merge_manage_box.add(
            self.merge_operation_box,
            self.merge_divider,
            self.merge_reslut_box
        )
        self.wallet_main_box.add(
            self.wallet_manage_box,
            self.merge_manage_box
        )
        await asyncio.sleep(1)
        self.show()



    async def scan_utxos(self, button):
        self.scan_button.enabled = False
        if os.path.exists(self.db_path):
            scan_addresses = self.client.listAddressgroupPings()
            account_addresses = self.client.ListAddresses()
        else:
            scan_addresses = await self.command.listAddressgroupPings()
            scan_addresses = json.loads(scan_addresses)
            account_addresses = await self.command.ListAddresses()
            account_addresses = json.loads(account_addresses)

        if scan_addresses:
            flattened_addresses = [address_info for address_info_list in scan_addresses for address_info in address_info_list]
            filtered_addresses = [address_info for address_info in flattened_addresses if address_info[1] != 0]
            sorted_addresses = sorted(filtered_addresses, key=lambda x: x[1], reverse=True)
            self.total_amount = sum(address_info[1] for address_info in sorted_addresses)
            addresses_only = [address_info[0] for address_info in sorted_addresses]
        if account_addresses:
            main_addresees = [address_info for address_info in account_addresses]
        addresses_only = [address for address in addresses_only if address not in main_addresees]
        self.number_addresses = len(addresses_only)
        if self.number_addresses == 0:
            self.scan_button.enabled = True
            return
        else:
            self.scan_button.enabled = True
            self.json_addresses = addresses_only
            await self.display_merge_options()


    async def display_merge_options(self):
        self.merge_list_txt.text = f"Total amount : {self.total_amount:.8f} BTCZ in {self.number_addresses} addresses"
        self.merge_operation_box.remove(
            self.scan_button
        )
        self.merge_address_box.add(
            self.merge_select_address_txt,
            self.merge_select_address
        )
        self.merge_fee_box.add(
            self.merge_fee_txt,
            self.merge_fee_input
        )
        self.merge_buttons_box.add(
            self.cancel_button,
            self.merge_button
        )
        self.merge_operation_box.add(
            self.merge_address_box,
            self.merge_list_txt,
            self.merge_fee_box,
            self.merge_buttons_box
        )


    async def verify_merge_inputs(self, button):
        self.cancel_button.enabled = False
        self.merge_button.enabled = False
        selected_address = self.merge_select_address.value.merge_select_address
        if not self.merge_fee_input.value:
            tx_fee = 0.0001
        else:
            tx_fee = self.merge_fee_input.value
        await self.start_merge_operation(selected_address, tx_fee)

    

    async def start_merge_operation(self, address, tx_fee):
        if os.path.exists(self.db_path):
            operation = self.client.z_mergeToaAdress(
                self.json_addresses,
                address,
                tx_fee
            )
        else:
            self.json_addresses = json.dumps(self.json_addresses)
            operation = await self.command.z_mergeToaAdress(
                self.json_addresses,
                address,
                tx_fee
            )
            if operation:
                operation = json.loads(operation)
        if operation is not None:
            remainingUTXOs = operation.get("remainingUTXOs")
            remainingTransparentValue = operation.get("remainingTransparentValue")
            mergingUTXOs = operation.get("mergingUTXOs")
            mergingTransparentValue = operation.get("mergingTransparentValue")
            operationID = operation.get("opid")
            await self.update_operation_status(
                remainingUTXOs,
                remainingTransparentValue,
                mergingUTXOs,
                mergingTransparentValue,
                operationID
            )
        else:
            self.error_dialog(
                "Error...",
                "z_mergetoaddress is disabled.\nTo enable it, add these two lines to bitcoinz.conf file\n\n-experimentalfeatures\n-zmergetoaddress"
            )
            await asyncio.sleep(1)
            self.cancel_button.enabled = True
            self.merge_button.enabled = True


    
    async def update_operation_status(self, remainingUTXOs, remainingTransparentValue, mergingUTXOs, mergingTransparentValue, operationID):
        self.remaining_utxos.text = f"remainingUTXOs : {remainingUTXOs}"
        self.remaining_value.text = f"remainingValue : {self.system.format_balance(remainingTransparentValue)}"
        self.merging_utxos.text = f"mergingUTXOs : {mergingUTXOs}"
        self.merging_value.text = f"mergingValue : {self.system.format_balance(mergingTransparentValue)}"
        self.operation_id_output.value = f"OperationID : {operationID}"
        while True:
            if os.path.exists(self.db_path):
                operation_status = self.client.z_getOperationStatus(operationID)
            else:
                operation_status = await self.command.z_getOperationStatus(operationID)
                operation_status = json.loads(operation_status)
            if operation_status is not None:
                status = operation_status[0].get('status')
                if status == "success":
                    await asyncio.sleep(3)
                    self.remaining_utxos.text = f"remainingUTXOs :"
                    self.remaining_value.text = f"remainingValue :"
                    self.merging_utxos.text = f"mergingUTXOs :"
                    self.merging_value.text = f"mergingValue :"
                    self.operation_id_output.value = ""
                    await self.cancel_merge_utxos(None)
                    return
            await asyncio.sleep(5)


    async def cancel_merge_utxos(self, button):
        self.number_addresses = None
        self.total_amount = None
        self.json_addresses = None
        self.merge_operation_box.remove(
            self.merge_address_box,
            self.merge_list_txt,
            self.merge_fee_box,
            self.merge_buttons_box
        )
        self.merge_operation_box.add(
            self.scan_button
        )
        
            


    async def switch_to_transparent(self, button):
        self.transaction_mode = "transparent"
        transparent_address = await self.get_transparent_addresses()
        self.select_address.style.color = YELLOW
        self.merge_select_address.style.color = YELLOW
        self.select_address.items = transparent_address
        self.merge_select_address.items = transparent_address
        self.switch_button_box.remove(
            self.transparent_button,
            self.shielded_icon
        )
        self.switch_button_box.add(
            self.transparent_icon,
            self.shielded_button
        )
        
    async def switch_to_shielded(self, button):
        self.transaction_mode = "shielded"
        shielded_address = await self.get_shielded_addresses()
        self.select_address.style.color = CYAN
        self.merge_select_address.style.color = CYAN
        self.select_address.items = shielded_address
        self.merge_select_address.items = shielded_address
        self.switch_button_box.remove(
            self.transparent_icon,
            self.shielded_button
        )
        self.switch_button_box.add(
            self.transparent_button,
            self.shielded_icon
        )


    async def display_private_key(self, button):
        active_windows = list(self.app.windows)
        for view_window in active_windows:
            if view_window.title == "Import Key":
                self.app.current_window = self.import_window
                return
            elif view_window.title == "Key View":
                self.app.current_window = self.view_window
                return
        if not self.select_address.value:
            return
        address = self.select_address.value.select_address
        if self.transaction_mode == "transparent":
            if os.path.exists(self.db_path):
                result = self.client.DumpPrivKey(address)
            else:
                result = await self.command.DumpPrivKey(address)
        elif self.transaction_mode == "shielded":
            if os.path.exists(self.db_path):
                result = self.client.z_ExportKey(address)
            else:
                result = await self.command.z_ExportKey(address)
        if result is not None:
            self.view_key_txt = Label(
                "Private Key for selected address :",
                style=LabelStyle.private_key_txt
            )
            self.view_key_input = TextInput(
                    value=result,
                    style=InputStyle.private_key_input
            )
            self.copy_button = Button(
                "Copy",
                style=ButtonStyle.copy_button,
                enabled=True,
                on_press=self.copy_key_clipboard
            )
            self.view_box = Box(
                style=BoxStyle.import_box
            )
            self.view_box.add(
                self.view_key_txt,
                self.view_key_input,
                self.copy_button
            )
            self.view_window = Window(
                title="Key View",
                size=(400, 100),
                minimizable=False,
                resizable=False
            )
            position_center = self.system.windows_screen_center(self.view_window.size)
            self.view_window.position = position_center
            self.view_window.content = self.view_box
            self.view_window.show()


    async def display_import_window(self, button):
        active_windows = list(self.app.windows)
        for import_window in active_windows:
            if import_window.title == "Key View":
                self.app.current_window = self.view_window
                return
            elif import_window.title == "Import Key":
                self.app.current_window = self.import_window
                return
        self.import_key_txt = Label(
            "Private Key :",
            style=LabelStyle.private_key_txt
        )
        self.import_key_input = PasswordInput(
            placeholder="Paste your private key",
            style=InputStyle.private_key_input
        )
        self.rescan_option = Switch(
            "rescan transactions (This can take minutes to complete)",
            style=SwitchStyle.rescan_option
        )
        self.confirm_key_button = Button(
            "Import",
            style=ButtonStyle.confirm_key_button,
            enabled=True,
            on_press=self.import_private_key
        )
        self.import_button_box = Box(
            style=BoxStyle.import_button_box
        )
        self.import_box = Box(
            style=BoxStyle.import_box
        )
        self.import_button_box.add(
            self.confirm_key_button
        )
        self.import_box.add(
            self.import_key_txt,
            self.import_key_input,
            self.rescan_option,
            self.import_button_box
        )
        self.import_window = Window(
            title="Import Key",
            size=(400, 130),
            minimizable=False,
            resizable=False
        )
        position_center = self.system.windows_screen_center(self.import_window.size)
        self.import_window.position = position_center
        self.import_window.content = self.import_box
        self.import_window.show()



    async def import_private_key(self, button):
        if not self.import_key_input.value:
            self.error_dialog(
                "Empty input...",
                "Private key is missing."
            )
            self.import_key_input.focus()
            return
        key = self.import_key_input.value
        
        self.transactions_list_option.enabled = False
        self.transparent_button.enabled = False
        self.shielded_button.enabled = False
        self.select_address.enabled = False
        self.new_address_button.enabled =False
        self.import_window.on_close = self.disable_closing_window
        self.import_key_input.readonly = True
        self.rescan_option.enabled = False
        self.import_button_box.remove(
            self.confirm_key_button
        )
        self.import_button_box.add(
            self.bitcoinz_coin
        )

        if self.rescan_option.value is True:

            rescan = True
        else:
            rescan = False

        if self.transaction_mode == 'transparent':
            if os.path.exists(self.db_path):
                result = self.client.ImportPrivKey(key, rescan)
            else:
                result = await self.command.ImportPrivKey(key, rescan)
        elif self.transaction_mode == "shielded":
            if os.path.exists(self.db_path):
                result = self.client.z_ImportKey(key, rescan)
            else:
                result = await self.command.z_ImportKey(key, rescan)

        if result is not None:
            await self.update_import_window()  
        else:
            self.error_dialog(
                "Error...",
                "Invalid private key encoding"
            )
            await self.update_import_window()

    
    async def update_import_window(self):
        self.transactions_list_option.enabled = True
        self.transparent_button.enabled = True
        self.shielded_button.enabled = True
        self.select_address.enabled = True
        self.new_address_button.enabled =True
        self.import_window.on_close = None
        self.import_key_input.readonly = False
        self.import_key_input.value = ""
        self.rescan_option.enabled = True
        self.import_button_box.remove(
            self.bitcoinz_coin
        )
        self.import_button_box.add(
            self.confirm_key_button
        )

        await self.update_addresses_list(None)


    
    async def import_wallet_file(self, button):
        async def on_confirm(window, path):
            if path:
                selected_file = str(path)
                backup_name = f"wallet{datetime.today().strftime('%d%m%Y%H%M%S')}"
                if os.path.exists(self.db_path):
                #Exports all wallet keys, for taddr and zaddr, in a human-readable format.
                    backup = self.client.z_exportWallet(backup_name)
                else:
                    backup = await self.command.z_exportWallet(backup_name)
                if backup:
                    self.info_dialog(
                        "Impoting wallet...",
                        "This operation may take minutes to complete, please wait..."
                    )
                    await asyncio.sleep(1)
                    if os.path.exists(self.db_path):
                        #Imports taddr and zaddr keys from a wallet export file
                        self.client.z_importWallet(selected_file)
                    else:
                        await self.command.z_importWallet(selected_file)
                else:
                    self.error_dialog(
                        "Error...",
                        "-exportdir is not set in bitcoinz.conf file."
                    )
                    return

        self.open_file_dialog(
            title="Select file...",
            file_types=["*"],
            initial_directory=self.app.paths.config,
            multiple_select=False,
            on_result=on_confirm
        )

            

    async def get_transparent_addresses(self):
        if os.path.exists(self.db_path):
            addresses_data = self.client.ListAddresses()
        else:
            addresses_data = await self.command.ListAddresses()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            address_items = [(address_info, address_info) for address_info in addresses_data]
        else:
            address_items = []
        
        return address_items
        

    async def get_shielded_addresses(self):
        if os.path.exists(self.db_path):
            addresses_data = self.client.z_listAddresses()
        else:
            addresses_data = await self.command.z_listAddresses()
            addresses_data = json.loads(addresses_data)
        if addresses_data is not None:
            address_items = [(address, address) for address in addresses_data]
        else:
            address_items = []
        return address_items
    

    async def generate_new_address(self, button):
        self.new_address_button.enabled = False
        if self.transaction_mode == "transparent":
            if os.path.exists(self.db_path):
                new_address = self.client.getNewAddress()
            else:
                new_address = await self.command.getNewAddress()
        
        elif self.transaction_mode == "shielded":
            if os.path.exists(self.db_path):
                new_address = self.client.z_getNewAddress()
            else:
                new_address = await self.command.z_getNewAddress()

        if new_address is not None:
            self.info_dialog(
                "New Address",
                f"New address generated :\n{new_address}"
            )
            await self.update_addresses_list(new_address)
        self.new_address_button.enabled = True


    async def update_addresses_list(self, address):

        if self.transaction_mode == "transparent":
            transparent_address = await self.get_transparent_addresses()
            self.select_address.style.color = YELLOW
            self.select_address.items = transparent_address
            self.merge_select_address.items = transparent_address

        elif self.transaction_mode == "shielded":
            shielded_address = await self.get_shielded_addresses()
            self.select_address.style.color = CYAN
            self.select_address.items = shielded_address
            self.merge_select_address.items = shielded_address
        if address is not None:  
            self.select_address.value = self.select_address.items.find(address)

    

    async def display_address_info(self, selection):
        if not self.select_address.value:
            return 
        address = self.select_address.value.select_address
        
        if len(self.address_manage_box.children) > 0:
            self.address_manage_box.remove(self.address_manage_box.children[0])

        self.address_manage_box.add(
            AddressInfo(
                self.app,
                address,
                self.transaction_mode
            )
        )
        


    async def copy_key_clipboard(self, button):
        Clipboard.SetText(self.view_key_input.value)
        self.copy_button.enabled = False
        await asyncio.sleep(1)
        self.copy_button.enabled = True



    def disable_closing_window(self, window):
        return
        


    def close_window(self, window):
        active_windows = list(self.app.windows)
        for open_window in active_windows:
            if open_window.title == "Import Key":
                self.app.current_window = self.import_window
                return
            elif open_window.title == "Key View":
                self.app.current_window = self.view_window
                return
        self.window_button.style.visibility = VISIBLE
        self.system.update_settings('wallet_window', False)
        self.close()