from expyriment import design, control, stimuli

exp = design.Experiment(name="Labeled Shapes")

control.set_develop_mode()
control.initialize(exp)


triangle = stimuli.Shape([(0, 43), (-25, -22), (25, -22)], 
                         colour=(200, 0, 200))
triangle_position = [-200, 0]
triangle.position = triangle_position

hex_coords = [
    (-25, 0), (-12.5, -22), (12.5, -22),
    (25, 0), (12.5, 22), (-12.5, 22)
]
hexagon = stimuli.Shape(hex_coords, colour=(255, 255, 0))
hexagon_position = [200, 0]
hexagon.position = hexagon_position

line_length = 50
line_width = 3
line_color = (255, 255, 255)

triangle_line = stimuli.Rectangle(size=(line_width, line_length), colour=line_color)
triangle_line.position = [triangle_position[0], triangle_position[1] + 25 + line_length/2]

hexagon_line = stimuli.Rectangle(size=(line_width, line_length), colour=line_color)
hexagon_line.position = [hexagon_position[0], hexagon_position[1] + 25 + line_length/2]

font_color = (255, 255, 255)

triangle_label = stimuli.TextLine("triangle", text_colour=font_color)
triangle_label.position = [triangle_line.position[0],
                           triangle_line.position[1] + line_length/2 + 20]

hexagon_label = stimuli.TextLine("hexagon", text_colour=font_color)
hexagon_label.position = [hexagon_line.position[0],
                          hexagon_line.position[1] + line_length/2 + 20]


control.start(subject_id=1)

triangle.present(clear=True, update=False)
hexagon.present(clear=False, update=False)
triangle_line.present(clear=False, update=False)
hexagon_line.present(clear=False, update=False)
triangle_label.present(clear=False, update=False)
hexagon_label.present(clear=False, update=True)

exp.keyboard.wait()

control.end()