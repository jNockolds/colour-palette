import turtle as t
from random import randint
import keyboard

#defining variables:

screen_width = 1080
screen_height = 9 * screen_width // 16
t.setup(screen_width, screen_height)
t.hideturtle()
t.tracer(0)
pen = t.Turtle()

# defining functions: 

def dec_to_hex(decimal):
    return f"{round(decimal):02X}" # X converts to hex, 02 makes sure it has 2 characters (with leading 0/s if necessary)

def hex_to_dec(hexadecimal):
    return int(hexadecimal, 16)

def get_brightness(colour):
    # parameter handling (convert all values to decimals):
    if isinstance(colour, str) and colour[0] == '#' and len(colour) == 7:
        r = hex_to_dec(colour[1:3])
        g = hex_to_dec(colour[3:5])
        b = hex_to_dec(colour[5:7])
    else:
        raise ValueError("Input colour must be a string starting with '#' and must be in hexadecimal with 6 digits")
    
    return ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255 # brightness is weighted by how sensitive human eyes are to red, green, and blue

def get_contrast_colour(colour, threshold_brightness=0.5):
    brightness = get_brightness(colour)

    if brightness > threshold_brightness:
        return "#000000"
    else:
        return "#FFFFFF"

def adjust_brightness(colour, brightness):
    if brightness < 0:
        raise ValueError("brightness must be >= 0")

    base_brightness = get_brightness(colour)
    if base_brightness == 0:
        r = dec_to_hex(int(255 * brightness))
        g = dec_to_hex(int(255 * brightness))
        b = dec_to_hex(int(255 * brightness))
        return f"#{r}{g}{b}" # returns grey with equivalent brightness
    
    scale_factor = brightness / base_brightness

    r = hex_to_dec(colour[1:3]) * scale_factor
    if r <= 255:
        r = dec_to_hex(r)
    else:
        r = "FF"

    g = hex_to_dec(colour[3:5]) * scale_factor
    if g <= 255:
        g = dec_to_hex(g)
    else:
        g = "FF"

    b = hex_to_dec(colour[5:7]) * scale_factor
    if b <= 255:
        b = dec_to_hex(b)
    else:
        b = "FF"

    return f"#{r}{g}{b}"

def sync_brightness(base_colour, alt_colour):
    """Returns alt_colour with its brightness equal to base_colour's brightness."""
    base_brightness = get_brightness(base_colour)
    return adjust_brightness(alt_colour, base_brightness)

def make_colour_palette(colour, maintain_brightness=False) -> list:
    # parameter handling (convert all values to hex strings):
    if isinstance(colour, str) and colour[0] == '#' and len(colour) == 7:
        r = colour[1:3].upper()
        g = colour[3:5].upper()
        b = colour[5:7].upper()
    else:
        raise ValueError("Input colour must be a string starting with '#' and must be in hexadecimal with 6 digits")
    
    # assigning all combinations of r, g, b:
    reds   = (r, r, g, g, b, b)
    greens = (g, b, r, b, r, g)
    blues  = (b, g, b, r, g, r)
    
    colours = []

    # generating palette:
    if maintain_brightness == False:
        for i in range(6):
            r = reds[i]
            g = greens[i]
            b = blues[i]
            colours.append(f"#{r + g + b}")
    else:
        for i in range(6):
            base_colour = colour
            alt_colour = f"#{reds[i]}{greens[i]}{blues[i]}"
            colours.append(sync_brightness(base_colour, alt_colour)) # keeping brightness constant
            
    return colours

def draw_screen_height_rectangles(turtle, colours):
    num_rectangles = len(colours)
    turtle.penup()
    turtle.goto((-screen_width / 2), screen_height / 2) # top left corner
    turtle.pendown()
    
    # drawing rectangles:
    for i in range(len(colours)):
        turtle.color(colours[i])
        turtle.begin_fill()
        turtle.goto(-(screen_width / 2) + i * (screen_width / num_rectangles) , -screen_height / 2) # bottom left corner
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), -screen_height / 2) # bottom right corner
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), screen_height / 2) # top right corner
        turtle.goto(-(screen_width / 2) + i * (screen_width / num_rectangles), screen_height / 2) # top left corner
        turtle.end_fill()

        # writing colour hex code in centre:
        turtle.goto(-(screen_width / 2) + (i + 0.5)* (screen_width / num_rectangles), 0) # centre of rectangle
        turtle.color(get_contrast_colour(colours[i])) # creating a contrasting text colour to make it almost always visible
        turtle.write(colours[i], align="center", font=('Arial', screen_height // 50, 'normal'))

        # moving to next rectangle starting point:
        turtle.penup()
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), screen_height / 2) # top right corner
        turtle.pendown()

def random_colour():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return f"#{r:02X}{g:02X}{b:02X}"

# drawing:

colours = make_colour_palette(random_colour(), True)

draw_screen_height_rectangles(pen, colours)

t.done() # keeps window open