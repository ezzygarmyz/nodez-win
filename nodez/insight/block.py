
from datetime import datetime
from typing import Iterable

from toga import (
    App,
    Box,
    Label,
    Divider
)
from toga.widgets.base import Widget
from toga.constants import Direction
from toga.colors import RED, GREEN

from .styles.box import BoxStyle
from .styles.label import LabelStyle
from .styles.divider import DividerStyle

from ..command import ClientCommands
from ..system import SystemOp


class BlockIndex(Box):
    def __init__(
            self,
            app:App,
            result: str | None = None,
            id: str | None = None,
            style= None,
            children: Iterable[Widget] | None = None
        ):
        style = BoxStyle.block_info
        super().__init__(id, style, children)
        self.app = app
        self.result = result
        self.command = ClientCommands(self.app)
        self.system = SystemOp(self.app)

        self.summary_title = Label(
            "- Summary -",
            style=LabelStyle.summary_title
        )
        self.transactions_title = Label(
            "- Transactions -",
            style=LabelStyle.summary_title
        )
        self.divider = Divider(
            direction=Direction.HORIZONTAL,
            style=DividerStyle.blocks_divider
        )
        self.blocks_title = Label(
            "",
            style=LabelStyle.blocks_title
        )
        self.blockhash_txt = Label(
            "BlockHash :",
            style=LabelStyle.block_blockhash_txt
        )
        self.blockhash = Label(
            "",
            style=LabelStyle.block_blockhash
        )
        self.blockhash_box = Box(
            style=BoxStyle.blockhash_box
        )
        self.number_txids_txt = Label(
            "Number Of Transactions :",
            style=LabelStyle.block_number_txids_txt
        )
        self.number_txids = Label(
            "",
            style=LabelStyle.block_number_txids
        )
        self.number_txids_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.blockheight_txt = Label(
            "Height :",
            style=LabelStyle.block_height_txt
        )
        self.blockheight = Label(
            "",
            style=LabelStyle.block_height
        )
        self.blockheight_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.block_reward_txt = Label(
            "Block Reward :",
            style=LabelStyle.block_reward_txt
        )
        self.block_reward = Label(
            "",
            style=LabelStyle.block_reward
        )
        self.block_reward_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.timestamp_txt = Label(
            "Timestamp :",
            style=LabelStyle.block_timestamp_txt
        )
        self.timestamp = Label(
            "",
            style=LabelStyle.block_timestamp
        )
        self.timestamp_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.merkleroot_txt = Label(
            "Merkle Root :",
            style=LabelStyle.block_merkleroot_txt
        )
        self.merkleroot = Label(
            "",
            style=LabelStyle.block_merkleroot
        )
        self.merkleroot_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.coinbase_txt = Label(
            "Coinbase :",
            style=LabelStyle.block_coinbase_txt
        )
        self.coinbase = Label(
            "",
            style=LabelStyle.block_coinbase
        )
        self.coinbase_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.difficulty_txt = Label(
            "Difficulty :",
            style=LabelStyle.block_difficulty_txt
        )
        self.difficulty = Label(
            "",
            style=LabelStyle.block_difficulty
        )
        self.difficulty_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.bits_txt = Label(
            "Bits :",
            style=LabelStyle.block_bits_txt
        )
        self.bits = Label(
            "",
            style=LabelStyle.block_bits
        )
        self.bits_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.size_txt = Label(
            "Size (bytes) :",
            style=LabelStyle.block_size_txt
        )
        self.size = Label(
            "",
            style=LabelStyle.block_size
        )
        self.size_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.version_txt = Label(
            "Version :",
            style=LabelStyle.block_version_txt
        )
        self.version = Label(
            "",
            style=LabelStyle.block_version
        )
        self.version_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.nonce_txt = Label(
            "Nonce :",
            style=LabelStyle.block_nonce_txt
        )
        self.nonce = Label(
            "",
            style=LabelStyle.block_nonce
        )
        self.nonce_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.solution_txt = Label(
            "Solution :",
            style=LabelStyle.block_solution_txt
        )
        self.solution = Label(
            "",
            style=LabelStyle.block_solution
        )
        self.solution_box = Box(
            style=BoxStyle.block_lines_box
        )
        self.block_details_divider = Divider(
            direction=Direction.VERTICAL,
            style=DividerStyle.block_details_divider
        )
        self.block_details_right_box = Box(
            style=BoxStyle.block_details_right_box
        )
        self.block_details_left_box = Box(
            style=BoxStyle.block_details_left_box
        )
        self.block_details_box = Box(
            style=BoxStyle.block_details_box
        )

        self.block_details_right_box.add(
            self.number_txids_box,
            self.blockheight_box,
            self.block_reward_box,
            self.timestamp_box,
            self.merkleroot_box,
            self.coinbase_box
        )
        self.block_details_left_box.add(
            self.difficulty_box,
            self.bits_box,
            self.size_box,
            self.version_box,
            self.nonce_box,
            self.solution_box
        )
        self.block_details_box.add(
            self.block_details_right_box,
            self.block_details_divider,
            self.block_details_left_box
        )

        self.app.add_background_task(
            self.get_block_info
        )


    async def get_block_info(self, widget):
        blockhash = self.result.get('hash')
        blockheight = self.result.get('height')
        txids = self.result.get('tx', [])
        number_txids = len(txids)
        block_tx = txids[0].get('vout', [])
        block_reward = 0.0
        for block in block_tx:
            vout_value = float(block.get('value', 0.0))
            block_reward += vout_value
        timestamp = self.result.get('time')
        formated_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        merkleroot = self.result.get('merkleroot')
        block_vin = txids[0].get('vin', [])
        coinbase = block_vin[0].get('coinbase')
        difficulty = self.result.get('difficulty')
        bits = self.result.get('bits')
        size = self.result.get('size')
        version = self.result.get('version')
        nonce = self.result.get('nonce')
        solution = self.result.get('solution')
        self.blocks_title.text = f"Block #{blockheight}"
        self.blockhash.text = blockhash
        self.number_txids.text = str(number_txids)
        self.blockheight.text = str(blockheight)
        self.block_reward.text = f"{int(block_reward)} BTCZ"
        self.timestamp.text = formated_time
        self.merkleroot.text = f"{merkleroot[:25]}..."
        self.coinbase.text = f"{coinbase[:25]}..."
        self.difficulty.text = f"{difficulty:.6f}"
        self.bits.text = str(bits)
        self.size.text = int(size)
        self.version.text = int(version)
        self.nonce.text = f"{nonce[:25]}..."
        self.solution.text = f"{solution[:25]}..."

        self.blockhash_box.add(
            self.blockhash_txt,
            self.blockhash
        )
        self.number_txids_box.add(
            self.number_txids_txt,
            self.number_txids
        )
        self.blockheight_box.add(
            self.blockheight_txt,
            self.blockheight
        )
        self.block_reward_box.add(
            self.block_reward_txt,
            self.block_reward
        )
        self.timestamp_box.add(
            self.timestamp_txt,
            self.timestamp
        )
        self.merkleroot_box.add(
            self.merkleroot_txt,
            self.merkleroot
        )
        self.coinbase_box.add(
            self.coinbase_txt,
            self.coinbase
        )
        self.difficulty_box.add(
            self.difficulty_txt,
            self.difficulty
        )
        self.bits_box.add(
            self.bits_txt,
            self.bits
        )
        self.size_box.add(
            self.size_txt,
            self.size
        )
        self.version_box.add(
            self.version_txt,
            self.version
        )
        self.nonce_box.add(
            self.nonce_txt,
            self.nonce
        )
        self.solution_box.add(
            self.solution_txt,
            self.solution
        )
        self.add(
            self.blocks_title,
            self.blockhash_box,
            self.summary_title,
            self.divider,
            self.block_details_box,
            self.transactions_title
        )

        await self.get_transactions_details(txids)


    async def get_transactions_details(self, txids):
        transaction_boxes = []
        for txid_data in txids:
            txid = txid_data.get('txid')
            transaction_id = Label(
                txid,
                style=LabelStyle.block_transaction_id
            )
            transcation_confirmations = Label(
                f"",
                style=LabelStyle.transaction_confirmations
            )
            transcation_value = Label(
                "",
                style=LabelStyle.transaction_value
            )
            transaction_fee_txt = Label(
                "",
                style=LabelStyle.transaction_fee
            )
            transaction_details_box = Box(
                style=BoxStyle.addresses_box
            )
            confirmations_box = Box(
                style=BoxStyle.confirmations_box
            )
            transaction_box = Box(
                style=BoxStyle.block_txids_box
            )
            inputs_box = Box(
                style=BoxStyle.transaction_address_box
            )
            outputs_box = Box(
                style=BoxStyle.transaction_address_box
            )
            transaction_box.add(transaction_id)

            vout = txid_data.get('vout', [])
            if vout:
                total_vout_value = sum(vout_data.get('value', 0) for vout_data in vout)
                for vout_data in vout:
                    vout_value = vout_data.get('value')
                    script_pubkey = vout_data.get('scriptPubKey', {})
                    vout_addresses = script_pubkey.get('addresses', [])
                    if isinstance(vout_addresses, list) and len(vout_addresses) == 1:
                        vout_address = vout_addresses[0]
                    else:
                        vout_address = ', '.join(vout_addresses) if vout_addresses else 'Unknown'
                    vout_address = Label(
                        f"{vout_address}  {self.system.format_balance(vout_value)} BTCZ",
                        style=LabelStyle.transaction_vout_address
                    )
                    outputs_box.add(vout_address)
            else:
                total_vout_value = 0
                vout_address = Label(
                    f"No Outputs",
                    style=LabelStyle.transaction_vout_address
                )
                outputs_box.add(vout_address)
            vin = txid_data.get('vin', [])
            if vin:
                total_vin_value = sum(vin_data.get('value', 0) for vin_data in vin)
                for vin_data in vin:
                    vin_value = vin_data.get('value')
                    vin_address = vin_data.get('address')
                    if vin_value and vin_address:
                        vin_address = Label(
                            f"{vin_address}  {self.system.format_balance(vin_value)} BTCZ",
                            style=LabelStyle.transaction_vin_address
                        )
                    elif vin_value and vin_address is None:
                        vin_address = Label(
                            f"Unparsed address  {self.system.format_balance(vin_value)} BTCZ",
                            style=LabelStyle.transaction_vin_address
                        )
                    else:
                        vin_address = Label(
                            "No Inputs (Newly Generated Coins)",
                            style=LabelStyle.transaction_vin_address
                        )
                    inputs_box.add(vin_address)
            else:
                vin_address = Label(
                    "No Inputs",
                    style=LabelStyle.transaction_vin_address
                )
                inputs_box.add(vin_address)
            transaction_fee = total_vin_value - total_vout_value
            if transaction_fee < 0:
                tx_fee = ""
            elif transaction_fee > 1:
                tx_fee = "Fee : 0.0001 BTCZ"
            else:
                tx_fee = f"Fee : {self.system.format_balance(transaction_fee)} BTCZ"
            confirmations = self.result.get('confirmations', '0')
            if confirmations == "0" or confirmations is None:
                background_color = RED
                confirmations.text = f"Unconfirmed Tx"
            else:
                background_color = GREEN
                transcation_confirmations.text = f"Confirmations : {confirmations}"
            transcation_confirmations.style.background_color = background_color
            transaction_fee_txt.text = tx_fee
            transcation_value.text = f"{self.system.format_balance(total_vout_value)} BTCZ"
            transaction_details_box.add(
                inputs_box,
                outputs_box
            )
            confirmations_box.add(
                transaction_fee_txt,
                transcation_confirmations,
                transcation_value
            )
            transaction_box.add(
                transaction_details_box,
                confirmations_box
            )
            
            transaction_boxes.append(transaction_box)
        
        for box in transaction_boxes:
            self.add(box)