==PL==\n
Implementacja kontrolera rozmytego do sterowania paletką w klasycznej grze Pong. Uproszczona wersja implementacji jest dostępna na GitHubie, z którego zforkowałem projekt. Kontroler został zaimplementowany przy użyciu biblioteki scikit-fuzzy.

Kontroler ma dostęp do dwóch wartości: odległości pomiędzy środkiem piłki a środkiem paletki w wymiarze X i Y. Głównym celem kontrolera jest przechwytywanie piłki, nie pozwalając przeciwnikowi zdobyć bramki.

W porównaniu z klasyczną wersją, ta implementacja wprowadza nowy sposób zwiększania prędkości odbijanej piłki. Jeśli piłka zostanie odbita przy użyciu najbardziej skrajnego 25% paletki, jej prędkość wzrasta o 10%. Ze względu na ograniczenia prędkości paletki, naiwny przeciwnik może nie być w stanie nadążyć w pewnym momencie.


==EN==\n
Implementation of a fuzzy controller for controlling the paddle in the classic game Pong is available on GitHub, from which I forked the project. The controller is implemented using the scikit-fuzzy library.

The controller has access to two values: the distance between the ball's center and the paddle's center in the X and Y dimensions. The main goal of the controller is to intercept the ball, preventing the opponent from scoring goals.

In comparison to the classic version, this implementation introduces a new way of increasing the speed of the rebounded ball. If the ball is bounced using the most extreme 25% of the paddle, its speed increases by 10%. Due to the speed limitations of the paddle, a naive opponent may not be able to keep up at some point.
