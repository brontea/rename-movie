#!/usr/bin/python3
import os
from movie import Movie

for file in os.listdir("."):
    if os.path.isfile(file) and not file.endswith((".nfo", ".py", ".out", ".sh")):
        print(file)
        movie = Movie(file)
        movie.update()
        movie.rename()
        movie.write_nfo()

        if input("Continue[enter] or quit[q]? ").lower() == "q":
            break
        print()
