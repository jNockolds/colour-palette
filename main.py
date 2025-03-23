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

# defining functions (NOTE: all function colour parameters should be in hexadecimal in with format "#XXXXXX" (where the Xs are the rgb values)):

def dec_to_hex(decimal):
    return f"{round(decimal):02X}" # X converts to hex, 02 makes sure it has 2 characters (with leading 0/s if necessary)

def hex_to_dec(hexadecimal):
    return int(hexadecimal, 16)

def get_brightness(colour):
    """Returns a value in range [0, 1] (including both end points) which represents the apparent brightness of the given.
    \nUses the formula 'b = ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255' because those coefficients of r, g, and b represent approximately how much human eyes weight the brightness of each colour (at least according to this paper: https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/tdpf/1/1/art00005).
    """
    # parameter handling (convert all values to decimals):
    if isinstance(colour, str) and colour[0] == '#' and len(colour) == 7:
        r = hex_to_dec(colour[1:3])
        g = hex_to_dec(colour[3:5])
        b = hex_to_dec(colour[5:7])
    else:
        raise ValueError("Input colour must be a string starting with '#' and must be in hexadecimal with 6 digits")
    
    return ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255 # brightness is weighted by how sensitive human eyes are to red, green, and blue on average

def get_contrast_colour(colour, threshold_brightness=0.5):
    """Returns either black or white (in hexadecimal) depending on how bright the input colour is."""
    brightness = get_brightness(colour)

    if brightness > threshold_brightness:
        return "#000000"
    else:
        return "#FFFFFF"

def adjust_brightness(colour, brightness):
    """Returns an adjusted version of the input colour with the given brightness."""
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

def sync_brightness(source_colour, alt_colour):
    """Returns an adjusted version of alt_colour with its brightness equal to source_colour's brightness."""
    base_brightness = get_brightness(source_colour)
    return adjust_brightness(alt_colour, base_brightness)

def make_colour_palette(colour, maintain_brightness=True) -> list:
    """
    Returns a list of six colours (including the input colour) with similar appearances.
    \n Parameter/s:
    - maintain_brightness: if True, all colours will have the same apparent brightness level (as decided by adjust_brightness); if False, they won't necessarily.
    """
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

def draw_screen_height_rectangles(turtle, colours, show_text=True, text_size=screen_height//50):
    """
    Fills the screen with vertical rectangles, side by side, with a given list of colours. 
    \n Parameter/s:
    - show_text: if True, text showing the hex code of each colour will be rendered (in either black or white, depending on the brightness of the colour).
    """
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

        if show_text == True:
            # writing colour hex code in centre:
            turtle.goto(-(screen_width / 2) + (i + 0.5)* (screen_width / num_rectangles), 0) # centre of rectangle
            turtle.color(get_contrast_colour(colours[i])) # creating a contrasting text colour to make it almost always visible
            turtle.write(colours[i], align="center", font=('Arial', text_size, 'normal'))

        # moving to next rectangle starting point:
        turtle.penup()
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), screen_height / 2) # top right corner
        turtle.pendown()

def random_colour():
    """Returns a random colour in hexadecimal."""
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return f"#{r:02X}{g:02X}{b:02X}"

# drawing:

colour = random_colour() # input("Colour: ")
colours = make_colour_palette(colour, False)

draw_screen_height_rectangles(pen, colours)

# printing results:
print(f"Source colour: {colour}")
print(f"Companion colours: ", end='')
[print(x + ', ', end='') for x in colours[1:-1]] # looks nicer than just printing the list
print(colours[-1])

t.done() # keeps window open