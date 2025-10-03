import time
import struct


from machine import Pin, SPI


from drivers.lcd_driver import ST7789V2
from drivers.lcd_config import LCD_CONFIG, LCD_PINS, SPI_CONFIG
from drivers.lcd_constans import LCD_COLORS


def main():
    # Инициализация SPI с правильными пинами
    spi = SPI(SPI_CONFIG['BUS'],
              baudrate=SPI_CONFIG['BAUDRATE'],
              polarity=SPI_CONFIG['POLARITY'],
              phase=SPI_CONFIG['PHASE'],
              sck=Pin(LCD_PINS['SCK']),
              mosi=Pin(LCD_PINS['MOSI']),
              miso=LCD_PINS['MISO'])

    # Инициализация дисплея
    lcd = ST7789V2(spi,
                   LCD_CONFIG['WIDTH'],
                   LCD_CONFIG['HEIGHT'],
                   dc_pin=LCD_PINS['DC'],
                   rst_pin=LCD_PINS['RST'],
                   cs_pin=LCD_PINS['CS'],
                   backlight_pin=LCD_PINS['BL'],
                   xstart=LCD_CONFIG['X_START'],
                   ystart=LCD_CONFIG['Y_START'])

    while True:

        for color in LCD_COLORS:
            lcd.fill_color(LCD_COLORS[color])
            time.sleep(1)

        # lcd.set_window(50, 50, 80, 80)
        # lcd._write_data(struct.pack(">H", COLOR_RED) * (31 * 31))
        # time.sleep(1)


if __name__ == "__main__":
    main()
