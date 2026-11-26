"""Emit the single comment line this entry is built around.

The program has one job: place an exact, pre-agreed comment string into
``entry.txt`` inside the output folder, and nothing else.  It reads no
input files, reaches out to no network, and behaves the same way every
time it is launched, whatever the environment looks like.
"""

import os


# The comment is stored as two short phrases so the wording stays
# readable in the source while the joined result stays byte-exact.
_PHRASES = (
    "// This function passes its tests only because the tests",
    " were written after the bug shipped, and now they protect it.",
)


def _comment_bytes():
    """Return the comment line as UTF-8 bytes, with no line ending."""
    return "".join(_PHRASES).encode("utf-8")


def _output_folder():
    """Pick the destination folder, falling back to /output."""
    chosen = os.environ.get("OUTPUT_DIR") or "/output"
    return chosen


def _place_file(folder, payload):
    """Create the folder if needed, then write the payload as entry.txt.

    Only the one target file is touched; anything else already sitting
    in the folder is left exactly where it is.
    """
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    handle = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(handle, payload)
    finally:
        os.close(handle)
    os.chmod(target, 0o644)


def main():
    _place_file(_output_folder(), _comment_bytes())


if __name__ == "__main__":
    main()
