Implementacja kontrolera rozmytego do sterowania paletką w klasycznej grze Pong. Uproszczona wersja implementacji jest dostępna na GitHubie. Kontroler został zaimplementowany przy użyciu biblioteki scikit-fuzzy.

Kontroler ma dostęp do dwóch wartości: odległości pomiędzy środkiem piłki a środkiem paletki w wymiarze X i Y. Głównym celem kontrolera jest przechwytywanie piłki, nie pozwalając przeciwnikowi zdobyć bramki.

W porównaniu z klasyczną wersją, ta implementacja wprowadza nowy sposób zwiększania prędkości odbijanej piłki. Jeśli piłka zostanie odbita przy użyciu najbardziej skrajnego 25% paletki, jej prędkość wzrasta o 10%. Ze względu na ograniczenia prędkości paletki, naiwny przeciwnik może nie być w stanie nadążyć w pewnym momencie.
