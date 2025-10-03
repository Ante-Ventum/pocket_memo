# DISPLAY main config:
LCD_CONFIG = {
    'WIDTH': 135,
    'HEIGHT': 240,
    'X_START': 52,  # standart driver's buffer 240x240
    'Y_START': 40,  # so need custom offset for non-standart lcd
}


# DISPLAY pins config:
LCD_PINS = {
    'SCK': 36,
    'MOSI': 35,
    'MISO': None,
    'CS': 37,
    'RST': 33,
    'DC': 34,
    'BL': 38
}

# SPI bus config:
SPI_CONFIG = {
    'BUS': 1,
    'BAUDRATE': 40_000_000,
    'POLARITY': 0,
    'PHASE': 0,

}
