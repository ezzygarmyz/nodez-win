from toga.style.pack import Pack
from toga.colors import BLACK, WHITE


class InputStyle():


    private_key_input = Pack(
        font_size = 11,
        padding = 10,
        color = WHITE,
        background_color = BLACK
    )


    merge_fee_input = Pack(
        padding_top = 10,
        padding_left = 20,
        padding_right = 200,
        font_size = 11,
        color = WHITE,
        background_color = BLACK,
        flex = 1
    )


    operation_id_output = Pack(
        padding_top = 5,
        padding_left = 10,
        padding_right = 10,
        font_size = 10,
        color = WHITE,
        background_color = BLACK,
        width= 200
    )