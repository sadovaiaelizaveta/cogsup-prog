from expyriment import design, control, stimuli
import math

def create_polygon(n, side_length, color, position):
    angle = 2 * math.pi / n 
    coords = [(side_length * math.cos(i * angle), side_length * math.sin(i * angle)) for i in range(n)]
    polygon = stimuli.Shape(coords, colour=color)
    polygon.position = position
    return polygon

exp = design.Experiment(name="Labeled Shapes")
control.set_develop_mode()
control.initialize(exp)

triangle_position = [-200, 0]
triangle = create_polygon(3, 50, (200, 0, 200), triangle_position)

hexagon_position = [200, 0]
hexagon = create_polygon(6, 50, (255, 255, 0), hexagon_position)

def create_line_and_label(shape_position, line_length, label_text):
    line = stimuli.Rectangle(size=(3, line_length), colour=(255, 255, 255))
    line.position = [shape_position[0], shape_position[1] + 25 + line_length / 2]
    
    label = stimuli.TextLine(label_text, text_colour=(255, 255, 255))
    label.position = [line.position[0], line.position[1] + line_length / 2 + 20]
    
    return line, label

triangle_line, triangle_label = create_line_and_label(triangle_position, 50, "triangle")

hexagon_line, hexagon_label = create_line_and_label(hexagon_position, 50, "hexagon")

control.start(subject_id=1)

triangle.present(clear=True, update=False)
hexagon.present(clear=False, update=False)
triangle_line.present(clear=False, update=False)
hexagon_line.present(clear=False, update=False)
triangle_label.present(clear=False, update=False)
hexagon_label.present(clear=False, update=True)

exp.keyboard.wait()

control.end()