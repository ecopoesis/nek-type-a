# Natural Ergonomic Keyboard, Type A

One of the best keyboards ever made is the [Microsoft Natural Keyboard](https://en.wikipedia.org/wiki/Microsoft_Natural_Keyboard). 
Unfortunately modern versions of the natural keyboard are significantly worse then the original mid 90s versions. 
The goal of this project is to create a high-quality, open-source replacement for the natural keyboard.

<img src="drawings/qmk.svg" width="250" alt="Power by QMK">

## Goals

* Standard split-QWERTY layout mirroring the Microsoft Natural Keyboards
* No built-in number pad
* High quality mechanical switches
* Bluetooth or USB connection
* Plug and play (no-solder) microcontroller replacement
* Heirloom quality

## Design

The keyboard (and repo) is divided into the following parts:

* Body
* Electronics

### Body

<img src="drawings/top-view.svg" width="500" alt="NEK Type A">

The body has three major components: the aluminum unibody, the left and right steel switch plates and the acrylic access panel. 

Source files:
* `*.kbd.json` files are generated using the [keyboard_layout_editor.com](http://www.keyboard-layout-editor.com)
* `*.svg` and `*.dxf` files are built using [swillkb's Plate and Case Builder](http://builder.swillkb.com/) based on the `.kbd.json` files
  * The `*switch.*` files are the laser cutter templates
* `body.stl` and `body.step` are built from the [CadQuery](https://github.com/dcowden/cadquery) source file `body.py`. The easiest way to build this is to use the provided Docker image and `Makefile`:
  ```bash
    cd body && make
  ```    

### Electronics

The electronics are designed to be swappable. The left and right PCBs only contain the keyboard matrices and the ribbon connectors to the center PCB.

The PCBs can be made directly from the `BRD` files by [OSH Park](http://oshpark.com).

#### Left
[left.brd](eagle/nek-type-a/left.brd)

<img src="drawings/left-001-top.png" width="250" alt="Left PCB Rev 001 Top">
<img src="drawings/left-001-bottom.png" width="250" alt="Right PCB Rev 001 Top">

#### Right

#### Center
The center PCB connects to the matrices via a series of [MCP23008](https://www.microchip.com/wwwproducts/en/MCP23008) I/O expanders hooked to the microprocessor via the I2C bus.
The center is designed to use development boards that conform the [Adafruit](https://www.adafruit.com/feather) interface. 
The feather is connected via headers on the center PCB so it can be swapped for models with different connectivity in the future was standards evolve.