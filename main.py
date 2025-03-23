import turtle as t

colour = "#332299" # input("colour hex code: #").lower()

screen_width = 1000
screen_height = 600
t.setup(screen_width, screen_height)
t.hideturtle()
t.tracer(0)
pen = t.Turtle()

def dec_to_hex(decimal):
    conversion_string = "0123456789ABCDEF"
    hexadecimal = ""
    while decimal > 0:
        remainder = decimal % 16
        hexadecimal = conversion_string[remainder] + hexadecimal
        decimal //= 16

    return hexadecimal

def make_colour_palette(colour) -> list:
    # parameter handling:
    if isinstance(colour, tuple):
        if isinstance(colour[0], int) and colour[0] >= 0 and colour[0] <= 255:
            r = dec_to_hex(colour[0])
        if isinstance(colour[1], int) and colour[0] >= 0 and colour[0] <= 255:
            g = dec_to_hex(colour[1])
        if isinstance(colour[2], int) and colour[0] >= 0 and colour[0] <= 255:
            b = dec_to_hex(colour[2])
    elif isinstance(colour, str) and colour[0] == '#':
        if len(colour) == 4:
            r = colour[1].upper()
            g = colour[2].upper()
            b = colour[3].upper()
        elif len(colour) == 7:
            r = colour[1:3].upper()
            g = colour[3:5].upper()
            b = colour[5:7].upper()
        else:
            raise ValueError("Input colour must be a tuple for RGB or a string starting with '#' for hexadecimal")
    else:
        raise ValueError("Input colour must be a tuple for RGB or a string starting with '#' for hexadecimal")
    
    # assigning all combinations of r, g, b:
    reds   = (r, r, g, g, b, b)
    greens = (g, b, r, b, r, g)
    blues  = (b, g, b, r, g, r)
    
    colours = []

    # generating palette:
    for i in range(6):
        r = reds[i]
        g = greens[i]
        b = blues[i]
        colours.append(f"#{r + g + b}")

    return colours

def draw_screen_height_rectangles(turtle, colours):
    num_rectangles = len(colours)
    
    turtle.penup()
    turtle.goto((-screen_width / 2), screen_height / 2) # top left corner
    turtle.pendown()
    for i in range(len(colours)):
        turtle.color(colours[i])
        turtle.begin_fill()
        turtle.goto(-(screen_width / 2) + i * (screen_width / num_rectangles) , -screen_height / 2) # bottom left corner
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), -screen_height / 2) # bottom right corner
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), screen_height / 2) # top right corner
        turtle.goto(-(screen_width / 2) + i * (screen_width / num_rectangles), screen_height / 2) # top left corner
        turtle.end_fill()

        turtle.goto(-(screen_width / 2) + (i + 0.5)* (screen_width / num_rectangles), 0) # centre of rectangle
        # todo: change colour
        turtle.write(colours[i])
        turtle.goto(-(screen_width / 2) + (i + 1) * (screen_width / num_rectangles), screen_height / 2) # top right corner

# todo: generate random colour
colours = make_colour_palette("#6DCE81")

print(colours)
draw_screen_height_rectangles(pen, colours)












pen.screen.mainloop()