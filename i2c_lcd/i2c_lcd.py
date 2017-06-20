# -*- coding: utf-8 -*-

"""
GPL-licensed code found on GitHub Gists, contained below with some slight
adjustments. Taken 2017-3-26.

https://gist.github.com/DenisFromHR/cc863375a6e19dce359d#file-rpi_i2c_driver-py
"""

"""
Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic
Made available under GNU GENERAL PUBLIC LICENSE

# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1

"""

import smbus
from time import *

# TODO: Organize these in some better way, maybe a dict or something?
# LCD Address
# Default to 0x27, for RPi3 I2C device
ADDRESS = 0x27

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit


class i2c_device:
    """Class for communicating with I2C devices over SMBus.

    Used to help the lcd class communicate with an I2C device via SMBus.

    Args:
        addr (hex str): Hex address of I2C device
        port (int): port for SMBus
    """
    def __init__(self, addr=ADDRESS, port=1):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def write_cmd(self, cmd):
        """Write a single command.

        Args:
            cmd (hex str): Hex command.
        """
        self.bus.write_byte(self.addr, cmd)
        sleep(0.0001)


class lcd:
    """Class for interfacing with I2C LCD device."""
    def __init__(self, addr=ADDRESS):
        self.lcd_device = i2c_device(addr)
        # TODO: Why write all of these? Assuming they're necessary to init.
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)

    def lcd_strobe(self, data):
        """Clocks enable bit to latch command.

        Args:
            data: data to write
        """
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        sleep(.0005)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep(.0001)

    def lcd_write_four_bits(self, data):
        """Write four bits of data to lcd device.

        Args:
            data: data to write
        """
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        """Write a command to lcd.

        Args:
            cmd (hex str): Hex command.
            mode (int): Mode? Defaults to 0.
        """
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_write_char(self, charvalue, mode=1):
        """Writes char to lcd.

        Notes from original:
            "write a character to lcd (or character rom) 0x09:
            backlight | RS=DR<"

        Args:
            charvalue (int): ordinal value of character to write.
            mode (int): Mode? Defaults to 1.
        """
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
        # Couldn't we just do this?
        # self.lcd_write(charvalue, mode=1)

    def lcd_display_string(self, string, line):
        """Displays string on lcd screen.

        Args:
            string (str): String to be displayed.
            line (int): Line for string to be displayed on. Must be 1-4.
        """
        if line == 1:
            self.lcd_write(0x80)
        elif line == 2:
            self.lcd_write(0xC0)
        elif line == 3:
            self.lcd_write(0x94)
        elif line == 4:
            self.lcd_write(0xD4)
        else:
            raise Exception("Line parameter must be 1, 2, 3, or 4.")

        for char in string:
            self.lcd_write(ord(char), Rs)
            # Could we use lcd_write_char?
            # self.lcd_write_char(char, Rs)

    def lcd_clear(self):
        """Clear lcd and set to home."""
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)

    def backlight_on(self, set_to_on):
        """Define backlight as on/off.

        Args:
            set_to_on (bool): True sets backlight on, False sets off.
        """
        if set_to_on:
            self.lcd_device.write_cmd(LCD_BACKLIGHT)
        else:
            self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

    def lcd_load_custom_chars(self, fontdata):
        """Load custom characters from font data.

        Args:
            fontdata (char[]): font data, max 7 characters.
        """
        self.lcd_write(0x40)
        for line in fontdata:
            for char in line:
                self.lcd_write_char(char)

    def lcd_display_string_pos(self, string, line, pos):
        """Display string in precise position/offset.

        Args:
            string (str): String to be displayed.
            line (int): Line for string to be displayed on. Must be 1-4.
            pos (int): Offset for displaying string
        """
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos
        else:
            raise Exception("Line parameter must be 1, 2, 3, or 4.")

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), Rs)
            # Could we use lcd_write_char?
            # self.lcd_write_char(char, Rs)

