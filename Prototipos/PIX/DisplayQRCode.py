import board
import displayio
import terminalio
import adafruit_ili9341
from adafruit_display_text import label
import adafruit_miniqr
import PixCopiaCola
def bitmap_QR(matrix):
    # monochome (2 color) palette
    BORDER_PIXELS = 2

    # bitmap the size of the screen, monochrome (2 colors)
    bitmap = displayio.Bitmap(
        matrix.width + 2 * BORDER_PIXELS, matrix.height + 2 * BORDER_PIXELS, 2
    )
    # raster the QR code
    for y in range(matrix.height):  # each scanline in the height
        for x in range(matrix.width):
            if matrix[x, y]:
                bitmap[x + BORDER_PIXELS, y + BORDER_PIXELS] = 1
            else:
                bitmap[x + BORDER_PIXELS, y + BORDER_PIXELS] = 0
    return bitmap
    
qr = adafruit_miniqr.QRCode(qr_type=8, error_correct=adafruit_miniqr.L)

qr.add_data(PixCopiaCola.getCopiaCola(
  "jornadadodesenvolvimento@o2br.net",
  "0.01",
  "Andre da Silva Mesquita",
  "BRASILIA",
  "https://github.com/O2br/jornadadodesenvolvimento2021" ))

qr.make()

# generate the 1-pixel-per-bit bitmap
qr_bitmap = bitmap_QR(qr.matrix)

displayio.release_displays()
display_bus = displayio.ParallelBus(data0=board.IO8,
                                    reset=board.IO3,
                                    chip_select=board.IO4,
                                    command=board.IO5,
                                    write=board.IO6,
                                    read=board.IO7)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

# generate the 1-pixel-per-bit bitmap
qr_bitmap = bitmap_QR(qr.matrix)
# We'll draw with a classic black/white palette
palette = displayio.Palette(2)
palette[0] = 0xFFFFFF
palette[1] = 0x000000
# we'll scale the QR code as big as the display can handle
scale = min(
    320 // qr_bitmap.width, 240 // qr_bitmap.height
)
# then center it!
pos_x = int(((320 / scale) - qr_bitmap.width) / 2)
pos_y = int(((240 / scale) - qr_bitmap.height) / 2)
qr_img = displayio.TileGrid(qr_bitmap, pixel_shader=palette, x=pos_x, y=pos_y)

splash = displayio.Group(scale=scale)
splash.append(qr_img)
display.show(splash)
