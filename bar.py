imort barcode
from barcode import EAN13
from barcode.writer import ImageWriter

with open("code.jpg", "wb") as f:
    EAN13('123456789561', writer=ImageWriter()).write(f)
    
