# mosaicG5 HAT V2 Hardware Revision

This document describes the V2 hardware revision of the mosaicG5 HAT and the changes made compared with the original V1 design.

V2 is a hardware-only revision. No changes were made to the software, communication protocol, or user operation of the board.

## Table of Content


## Design Files

| File | Description |
|---|---|
| [mosaicG5_RPi_HAT.kicad_pro](../Kicad/mosaicG5%20HAT/V2/mosaicG5_RPi_HAT.kicad_pro) | V2 KiCad project |
| [mosaicG5_RPi_HAT.kicad_sch](../Kicad/mosaicG5%20HAT/V2/mosaicG5_RPi_HAT.kicad_sch) | V2  KiCad schematic |
| [mosaicG5_RPi_HAT.kicad_pcb](../Kicad/mosaicG5%20HAT/V2/mosaicG5_RPi_HAT.kicad_pcb) | V2  KiCad  PCB layout |
| [BOM](../Kicad/mosaicG5%20HAT/V2/BOM%20P3H_V2.xlsx) | mosaicG5 HAT V2 Bill of Materials |



## V2 Hardware Changes

| Change | V2 modification | Purpose |
|---|---|---|
| **ESD protection** | Added an ESD protection diode on the VBUS input | Protects the board against electrostatic discharge through the USB power connection |
| **Power filtering** | Added **L1 ferrite bead** between the ideal-diode stage and buck converter |Helps filter noise before it reaches the buck converter|
| **FTDI interface** | Rearranged the FTDI pins to follow the standard pin arrangement | Makes the interface more convenient and compatible with standard FTDI connections |
| **Buck converter output** | Increased from **3.6 V to 3.7 V** | Provides additional voltage headroom for the 3.3 V LDO |
| **LDO input margin** | Changed from **3.6 V - 3.3 V** to **3.7 V - 3.3 V** | Increases the voltage margin available to the LDO to maintain a stable 3.3 V output |

### FTDI Interface
<img src="../pictures/FTDI V2.png" width="50%">

<img src="../pictures/FTDI_PCB V2.png" width="50%">

The FTDI pin arrangement was changed to follow the standard FTDI pinout, making it easier to connect compatible FTDI cables and adapters while maintaining the same UART2 functionality described in the V1 FTDI section.


### What Remains Unchanged?

No changes were made to:

mosaic-G5 module
Raspberry Pi interface
UART functionality
PPS functionality
USB data interface
Antenna connections
LED functionality
Clock reference

These parts of the design remain as described in the V1 documentation.

### Does V2 still work with the existing user documentation?

Yes, V2 remains compatible with the existing mosaicG5 HAT V1 user documentation.

No software changes are required.

The communication interfaces and board functionality remain unchanged.

## Revision Summary

| Revision | Description |
|---|---|
| V1 | Initial hardware design |
| V2 | Hardware revision with improved design |