from toga.style.pack import Pack
from toga.colors import BLACK, YELLOW


class ButtonStyle():
    
    
    rpc_button = Pack(
        background_color = BLACK,
        padding_left = 20,
        padding_top = 25
    )
    
    local_button = Pack(
        background_color = BLACK,
        padding_left = 20,
        padding_top = 25
    )
    
    download_button = Pack(
        padding_top = 32,
        padding_left = 5,
        background_color = BLACK
    )
    
    social_button = Pack(
        background_color = BLACK
    )


    connect_button = Pack(
        padding_top = 15,
        background_color = BLACK,
        width = 116
    )


    start_button = Pack(
        color = YELLOW,
        background_color = BLACK,
        padding_top = 15,
        padding_left = 10,
        padding_right = 10
    )