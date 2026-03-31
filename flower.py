import turtle

def draw_petal(t, radius):
    """Draws a single petal using two arcs."""
    for _ in range(2):
        t.circle(radius, 60)  # Draw an arc of 60 degrees
        t.left(120)           # Turn to draw the other side of the petal

def draw_flower():
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("white")
    
    # Create the turtle
    flower = turtle.Turtle()
    flower.speed(10)
    
    # 1. Draw the Stem
    flower.color("green")
    flower.pensize(5)
    flower.penup()
    flower.goto(0, -200)
    flower.pendown()
    flower.goto(0, -50)
    
    # 2. Draw the Petals
    flower.penup()
    flower.goto(0, 0)
    flower.pendown()
    flower.color("pink")
    flower.pensize(2)
    
    # Draw 6 petals
    for _ in range(6):
        draw_petal(flower, 100)
        flower.left(60)
        
    # 3. Draw the Center
    flower.penup()
    flower.goto(0, -20)  # Adjust to center the circle
    flower.pendown()
    flower.color("yellow")
    flower.begin_fill()
    flower.circle(20)
    flower.end_fill()
    
    # Hide the turtle and keep window open
    flower.hideturtle()
    screen.mainloop()

if __name__ == "__main__":
    draw_flower()
