import time
import struct


from machine import Pin, SPI


class info():
    driver_type = 'st7789v2'


# Определения команд для ST7789V
_ST7789_SWRESET = b"\x01"
_ST7789_SLPOUT = b"\x11"
_ST7789_COLMOD = b"\x3A"
_ST7789_MADCTL = b"\x36"
_ST7789_CASET = b"\x2A"
_ST7789_RASET = b"\x2B"
_ST7789_RAMWR = b"\x2C"
_ST7789_DISPON = b"\x29"
_ST7789_INVON = b"\x21"


class ST7789V2:
    def __init__(self, spi_bus, width, height, dc_pin, rst_pin, cs_pin=None, backlight_pin=None, rotation=0, xstart=0, ystart=0):
        self.spi = spi_bus
        self.width = width
        self.height = height
        self.dc = Pin(dc_pin, Pin.OUT)
        self.rst = Pin(rst_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT) if cs_pin else None
        self.bl = Pin(backlight_pin, Pin.OUT) if backlight_pin else None

        self.xstart = xstart
        self.ystart = ystart

        self._rotation = rotation
        self._init_display()

    def _write_command(self, command):
        """Отправка команды на дисплей"""
        if self.cs:
            self.cs(0)
        self.dc(0)
        self.spi.write(command)
        if self.cs:
            self.cs(1)

    def _write_data(self, data):
        """Отправка данных на дисплей"""
        if self.cs:
            self.cs(0)
        self.dc(1)
        self.spi.write(data)
        if self.cs:
            self.cs(1)

    def _write_init_sequence(self):
        """Последовательность инициализации для ST7789V2"""
        # Аппаратный сброс
        self.rst(1)
        time.sleep_ms(10)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(120)  # Ожидание после сброса

        # Команды инициализации
        self._write_command(_ST7789_SWRESET)  # Программный сброс
        time.sleep_ms(120)

        self._write_command(_ST7789_SLPOUT)   # Выход из спящего режима
        time.sleep_ms(120)

        # Установка цветового режима (RGB565)
        self._write_command(_ST7789_COLMOD)
        self._write_data(b"\x55")  # 0x55 = 16 бит на пиксель
        time.sleep_ms(10)

        # Установка направления обновления памяти (MADCTL)
        # Значение может потребовать настройки под конкретный дисплей
        self._write_command(_ST7789_MADCTL)
        self._write_data(b"\x00")  # Базовая ориентация
        time.sleep_ms(10)

        # Включение инверсии цветов (часто требуется)
        self._write_command(_ST7789_INVON)
        time.sleep_ms(10)

        # Включение дисплея
        self._write_command(_ST7789_DISPON)
        time.sleep_ms(120)

        # Включение подсветки, если пин указан
        if self.bl:
            self.bl(1)

    def _init_display(self):
        """Полная инициализация дисплея"""
        self._write_init_sequence()

    def set_window(self, x0, y0, x1, y1):
        """Установка окна для записи пикселей"""
        x0 += self.xstart
        x1 += self.xstart
        y0 += self.ystart
        y1 += self.ystart

        self._write_command(_ST7789_CASET)
        self._write_data(struct.pack(">HH", x0, x1))

        self._write_command(_ST7789_RASET)
        self._write_data(struct.pack(">HH", y0, y1))

        self._write_command(_ST7789_RAMWR)

    def fill_color(self, color):
        """Заливка экрана указанным цветом"""
        # Установка окна на весь экран
        self.set_window(0, 0, self.width - 1, self.height - 1)

        # Подготовка данных пикселя
        pixel_data = struct.pack(">H", color)

        # Отправка цвета для всех пикселей
        buffer = pixel_data * (self.width * self.height)
        self._write_data(buffer)
