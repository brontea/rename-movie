#!/usr/bin/python3
import datetime, os, re, readline

class Movie:
    """Model a movie filename for Kodi."""

    # new file template (for correct movie filename an nfo filename)
    new_filename_template = "{0}({1}).{2}"

    # NFO file content template
    nfo_template = """
    <?xml version="1.0" encoding="utf-8"?>
    <movie>
      <title>{0}</title>
      <year>{1}</year>
    </movie>
    """

    def __init__(self, filename):
        """Initialize attributes."""
        self.filename = filename
        self.name, self.year, self.suffix = self.name_year_suffix()

    def name_year_suffix(self):
        """Get movie name, year and suffix from filename."""
        parts = self.filename.rsplit(".", 1)
        # if there is no suffix, add empty one
        if len(parts) == 1:
            parts.append("")
        suffix = parts[1]

        # if year found I can split by year
        year_found = re.search("((?:19|20)\d{2})", parts[0])
        if year_found:
            year = year_found.group(1)
            name = parts[0].partition(year)[0]
        else:
            year = str(datetime.datetime.now().year)
            name = parts[0]

        # sanitize name
        name = name[:1].upper() + name[1:] # only first letter uppercase
        name = name.translate(str.maketrans({".": " ", "_": " ", "-": " "}))
        name = name.rstrip('(')
        name = ' '.join(name.split()) # remove extra(including trailing) spaces

        return (name, year, suffix)

    def user_input(self, prompt, prefill=''):
        """User input with prefilled value."""
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()

    def update(self):
        """Update attributes from user input."""
        self.name = self.user_input("Enter new movie name: ", self.name)
        self.year = self.user_input("Enter year of the movie: ", self.year)
        self.suffix = self.user_input("Enter movie suffix: ", self.suffix)

    def rename(self):
        """Rename movie file."""
        new_filename = Movie.new_filename_template.format(self.name, self.year, self.suffix)
        if os.path.isfile(self.filename):
            print(f"Renaming {self.filename} to {new_filename}...")
            os.rename(self.filename, new_filename)

    def write_nfo(self):
        """Write movie nfo file."""
        nfo_filename = Movie.new_filename_template.format(self.name, self.year, "nfo")
        nfo_content = Movie.nfo_template.format(self.name, self.year).strip()
        print(f"Creating .nfo file...")
        with open(nfo_filename, "w") as nfo:
            nfo.write(nfo_content)
