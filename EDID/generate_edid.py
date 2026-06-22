#!/usr/bin/env python3
"""
Loewe Technologies GmbH - 32" CRT VGA Adapter Board EDID Generator
Calculates and prints a perfectly aligned, 128-byte EDID v1.3 block.

"""

# =========================================================================
# CONFIGURATION
# Set this to True to use standard CVT timings matching the 'cvt' command output (31.50 MHz).
# Set to False to use the conservative 31.75 MHz timings.
# =========================================================================
USE_OFFICIAL_CVT_UTILITY_TIMINGS = False

def generate_edid():
    # Initialize a clean 128-byte block
    edid = [0] * 128

    # 1. Fixed Header (Bytes 0-7)
    edid[0:8] = [0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]

    # 2. Vendor / Product Identification (Bytes 8-17)
    # Manufacturer ID: "LOE" compressed (0x31E5)
    edid[8] = 0x31
    edid[9] = 0xE5
    edid[10:12] = [0x01, 0x00]              # Product Code: 1
    edid[12:16] = [0x00, 0x00, 0x00, 0x00]  # Serial Number: None
    edid[16] = 26                           # Week of Manufacture: 26
    edid[17] = 36                           # Year of Manufacture: 2026 (1990 + 36)

    # 3. EDID Structure Version & Revision (Bytes 18-19)
    edid[18] = 1
    edid[19] = 3

    # 4. Basic Display Parameters & Features (Bytes 20-24)
    edid[20] = 0x00  # Analog display, 0.700V/0.300V, separate sync
    edid[21] = 0x47  # Max Horizontal Image Size = 71 cm (32" 16:9)
    edid[22] = 0x28  # Max Vertical Image Size = 40 cm (32" 16:9)
    edid[23] = 0x78  # Display Gamma = 2.20
    edid[24] = 0x00  # Feature Support (Monochrome/grayscale, no DPMS)

    # 5. Color Characteristics (Bytes 25-34)
    edid[25:35] = [0xEE, 0x91, 0xA3, 0x54, 0x4C, 0x99, 0x26, 0x0F, 0x50, 0x54]

    # 6. Established Timings (Bytes 35-37)
    # Byte 35: Bit 7 (720x400@70Hz) & Bit 5 (640x480@60Hz) -> 0xA0
    # Byte 36: 0x00
    # Byte 37: 0x00
    edid[35] = 0xA0
    edid[36] = 0x00
    edid[37] = 0x00

    # 7. Standard Timings (Bytes 38-53)
    for i in range(38, 54):
        edid[i] = 0x01

    # 8. Descriptor Block 1: DTD 1 (Bytes 54-71) -> 848x480 @ 60Hz
    if USE_OFFICIAL_CVT_UTILITY_TIMINGS:
        # 31.50 MHz Target Layout (Matches 'cvt 848 480 60')
        # H.Active: 848 (0x350), H.Blank: 208 (0x0D0)
        # V.Active: 480 (0x1E0), V.Blank: 20 (0x014)
        dtd1 = [
            0x4E, 0x0C,  # Pixel Clock: 31.50 MHz (0x0C4E)
            0x50,        # H Active Lower 8 bits (0x50)
            0xD0,        # H Blanking Lower 8 bits (0xD0)
            0x30,        # H Active High Nibble (3) | H Blanking High Nibble (0) -> 0x30
            0xE0,        # V Active Lower 8 bits (0xE0)
            0x14,        # V Blanking Lower 8 bits (0x14)
            0x10,        # V Active High Nibble (1) | V Blanking High Nibble (0) -> 0x10
            0x18,        # H Sync Front Porch Lower 8 bits (24 -> 0x18)
            0x50,        # H Sync Pulse Width Lower 8 bits (80 -> 0x50)
            0x3A,        # V Front Porch (3) | V Sync Pulse Width (10 -> 0x0A) -> 0x3A
            0x00,        # High nibbles for Porches/Syncs
            0x47,        # H Image Size (71 cm)
            0x28,        # V Image Size (40 cm)
            0x00,        # Image Size High Nibbles
            0x00,        # H Border (0)
            0x00,        # V Border (0)
            0x1C         # Flags: Progressive, Separate Sync, -H / +V
        ]
    else:
        # 31.75 MHz Target Layout (Conservative Retrace Layout)
        # H.Active: 848 (0x350), H.Blank: 176 (0x0B0)
        # V.Active: 480 (0x1E0), V.Blank: 37 (0x025)
        dtd1 = [
            0x67, 0x0C,  # Pixel Clock: 31.75 MHz (0x0C67)
            0x50,        # H Active Lower 8 bits (0x50)
            0xB0,        # H Blanking Lower 8 bits (0xB0)
            0x30,        # H Active High Nibble (3) | H Blanking High Nibble (0) -> 0x30
            0xE0,        # V Active Lower 8 bits (0xE0)
            0x25,        # V Blanking Lower 8 bits (0x25)
            0x10,        # V Active High Nibble (1) | V Blanking High Nibble (0) -> 0x10
            0x10,        # H Sync Front Porch Lower 8 bits (16 -> 0x10)
            0x50,        # H Sync Pulse Width Lower 8 bits (80 -> 0x50)
            0x3A,        # V Front Porch (3) | V Sync Pulse Width (10 -> 0x0A) -> 0x3A
            0x00,        # High nibbles for Porches/Syncs
            0x47,        # H Image Size (71 cm)
            0x28,        # V Image Size (40 cm)
            0x00,        # Image Size High Nibbles
            0x00,        # H Border (0)
            0x00,        # V Border (0)
            0x1C         # Flags: Progressive, Separate Sync, -H / +V
        ]
    
    edid[54:72] = dtd1

    # 9. Descriptor Block 2: Monitor Name (Bytes 72-89) -> "Loewe CRT"
    name_desc = [0x00, 0x00, 0x00, 0xFC, 0x00] 
    name_payload = list(b"Loewe CRT\n")
    name_desc.extend(name_payload)
    while len(name_desc) < 18:
        name_desc.append(0x20) 
    edid[72:90] = name_desc

    # 10. Descriptor Block 3: Dummy Block (Bytes 90-107)
    dummy_desc1 = [0x00, 0x00, 0x00, 0x10, 0x00]
    while len(dummy_desc1) < 18:
        dummy_desc1.append(0x00)
    edid[90:108] = dummy_desc1

    # 11. Descriptor Block 4: Dummy Block (Bytes 108-125)
    dummy_desc2 = [0x00, 0x00, 0x00, 0x10, 0x00]
    while len(dummy_desc2) < 18:
        dummy_desc2.append(0x00)
    edid[108:126] = dummy_desc2

    # 12. Extension Flag (Byte 126)
    edid[126] = 0x00

    # 13. Dynamic Checksum calculation (Byte 127)
    total_sum = sum(edid[:127])
    edid[127] = (256 - (total_sum % 256)) % 256

    # Structural Assertions
    assert len(edid) == 128, f"Error: EDID length is {len(edid)}, must be exactly 128!"
    assert sum(edid) % 256 == 0, "Error: Checksum calculation invalid!"

    print("".join(f"{b:02X}" for b in edid))

if __name__ == "__main__":
    generate_edid()