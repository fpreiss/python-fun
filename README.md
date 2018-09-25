# python-fun
This repository contains a couple of minimalistic python scripts for demonstration purposes.
## `automata/`
Some examples of cellular automata with a small linecount in mind.
### `automata/game_of_life.py`
An implementation of Conway's Game of Life, with fixed number of frames. The rules of the cellular automata are applied using a convolution of the world with a 3x3 kernel to the matrix containing the current state.
### `automata/1D_automata.py`
A 1-D cellular automata using the python standard library only. Accepts all [Wolfram Code][1] rules with S=2 and D=1 via the `-rule` command line argument. The logic of the automata is implemented using native python strings and lists as well as python mappings, lambda functions, tenary operators and binary representations. Output requires the terminal to display utf8-characters.
## `OpenGL-numpy/`
Interactive visualisation of 2D numpy-arrays using OpenGL (requires PyOpenGL).
### `OpenGL-numpy/gl_canvas_numpy.py`
A snake-like 'game' with the logic-part completely implemented in numpy, while the drawing and window-behaviour are taken care of by OpenGL/OpenGLUT.
My first program using OpenGL - implementation might not follow most recent standards. Roughly oriented on [this][2] example.
Controls:
```
<arrow-keys>: change direction
<r>         : reset
<p>         : pause
<Esc>/<q>   : quit
```

[1]: https://en.wikipedia.org/wiki/Wolfram_codew
[2]: https://wiki.delphigl.com/index.php/OpenGL_mit_GLUT
