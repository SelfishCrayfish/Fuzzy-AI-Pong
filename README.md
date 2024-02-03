Implementation of a fuzzy controller for controlling the paddle in the classic game Pong is available on GitHub, from which I forked the project. The controller is implemented using the scikit-fuzzy library.

The controller has access to two values: the distance between the ball's center and the paddle's center in the X and Y dimensions. The main goal of the controller is to intercept the ball, preventing the opponent from scoring goals.

In comparison to the classic version, this implementation introduces a new way of increasing the speed of the rebounded ball. If the ball is bounced using the most extreme 25% of the paddle, its speed increases by 10%. Due to the speed limitations of the paddle, a naive opponent may not be able to keep up at some point.
