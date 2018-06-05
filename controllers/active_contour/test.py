import numpy as np
import pandas as pd
from vispy import app
from vispy import gloo
from vispy.plot import Fig


input_loc_path = r"C:\Users\biophys\Desktop\dSTORM_2\slice2_1205_dSTORM_actin_647_2.txt"
loc_input_1 = pd.read_csv(input_loc_path, skiprows=1, header=None, delim_whitespace=True).as_matrix()
loc_input_1 = loc_input_1[:,:2]
loc_input_1 = np.array(loc_input_1, dtype=np.int32)
x = np.c_[
        np.linspace(-1.0, +1.0, 1000),
        np.random.uniform(-0.5, +0.5, 1000)]
c = app.Canvas(keys='interactive')

vertex = """
attribute vec2 a_position;
void main (void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""
fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""
program = gloo.Program(vertex, fragment)
program['a_position'] = x
@c.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)

@c.connect
def on_draw(event):
    gloo.clear((1,1,1,1))
    program.draw('line_strip')

c.show()
app.run();
program.draw()

