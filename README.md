![https://ci.appveyor.com/api/projects/status/github/wheeler-microfluidics/avr_helpers?branch=master&svg=true](https://ci.appveyor.com/api/projects/status/github/wheeler-microfluidics/avr_helpers?branch=master&svg=true)
# `avr_helpers` #

This package provides helper classes for interacting with the [AVR][1]
tool-chain.  It includes a copy of `avrdude` for Windows, and Linux _(32-bit
and 64-bit)_, along with the `avrdude.conf` file from the [Arduino 1.0.5
IDE][2].  This allows stand-alone flashing of compile `.hex` firmware files.

[1]: http://en.wikipedia.org/wiki/Atmel_AVR
[2]: http://arduino.cc/en/main/software


## `avrdude` API ##

The `avr_helpers.AvrDude` class implements an API for:

 - Scanning available serial ports for a connected device.
 - Flashing a `.hex` bit-stream file to an AVR device.

### `AvrDude` API Usage ###

    >>> from avr_helpers import AvrDude
    >>> AvrDude?
    Type:            type
    String form:     <class 'avr_helpers.AvrDude'>
    File:            ...
    Init definition: AvrDude(self, protocol, microcontroller, baud_rate, conf_path=None, port=None)
    Docstring:       ...
    >>> avr_dude = AvrDude('arduino', 'atmega168', '19200')
    >>> # `-D` disables erase cycle to speed up programming.
    >>> stdout, stderr = avr_dude.flash('blink.hex', ['-D'])
    >>> print stdout

    >>> print stderr

    avrdude-x64: AVR device initialized and ready to accept instructions

    Reading | ################################################## | 100% 0.00s

    avrdude-x64: Device signature = 0x1e9406
    avrdude-x64: reading input file "blink.hex"
    avrdude-x64: writing flash (1056 bytes):

    Writing | ################################################## | 100% 0.76s

    avrdude-x64: 1056 bytes of flash written
    avrdude-x64: verifying flash memory against blink.hex:
    avrdude-x64: load data flash data from input file blink.hex:
    avrdude-x64: input file blink.hex contains 1056 bytes
    avrdude-x64: reading on-chip flash data:

    Reading | ################################################## | 100% 0.68s

    avrdude-x64: verifying ...
    avrdude-x64: 1056 bytes of flash verified

    avrdude-x64 done.  Thank you.

Note that since the `avrdude.conf` file from the Arduino IDE is included in the
`avr_helpers` package, the `arduino` protocol may be used, allowing easy
flashing of pre-compiled `.hex` files to Arduino devices.
