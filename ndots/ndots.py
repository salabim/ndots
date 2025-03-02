import collections

__version__ = "1.0.0"

__all__ = "fifteendots fiftydots twentyfourdots".split()


def available_fonts():
    """
    all available fonts

    Returns
    -------
    available fonts : tuple
    """
    return (fifteendots, fiftydots, twentyfourdots)


class _Dots:
    def __init__(self, height, width, name, spec):
        self._chartable = collections.defaultdict(list)
        for line in spec.splitlines():
            if line:
                if len(line) == 1:
                    char = line
                else:
                    self._chartable[char].append([vl == "*" for vl in line])
        self._height = height
        self._width = width
        self._name = name

    def width(self):
        """
        width of this font

        Returns
        -------
            width : int
        """
        return self._width

    def height(self):
        """
        height of this font

        Returns
        -------
            height : int
        """

        return self._height

    def name(self):
        """
        name of this font

        Returns
        -------
            name : str
        """

        return self._name

    def has_char(self, c):
        """
        availabiliy of character

        Parameters
        ----------
        c : str
            character to check

        Returns
        -------
        True, if available; False, otherwise : bool
        """
        return c in self._chartable

    def _grid_char(self, c, default=" ", proportional=False, narrow=False):
        if not self.has_char(c):
            c = default
        chartable = self._chartable[c]
        if proportional:
            filled_cols = [i for i in range(self._width) if any((chartable[y][i] if i < len(chartable[y]) else False) for y in range(self._height))]
            if not filled_cols:  # blank
                filled_cols = [0, 1 - bool(narrow)]
        else:
            filled_cols = [0, self._width - 1]

        return [line[filled_cols[0] : filled_cols[-1] + 1] for line in chartable]

    def _str_to_pixel_lines(self, s, default=" ", intra=1, proportional=False, narrow=False):
        result = []
        for y in range(self._height):
            line = []
            for i, c in enumerate(s):
                line.extend((i != 0) * intra * [False] + self._grid_char(c, default=default, proportional=proportional, narrow=narrow)[y])
            result.append(line)
        return result

    def number_of_pixels(self, s, default=" ", intra=1, proportional=False, narrow=False):
        """
        returns the length (in dots) of the text s in this font

        Parameters
        ----------
        s : str
            string to represent

        default : str
            if a character has no representation in the font, it will be replaced
            with default, that is a blank by default
            if the length is not 1, a ValueError will be raised

        intra : int
            number of dots between characters
            default is 1

        proportional : bool
            if proportional is False (default), all characters will be 5 dots wide
            if proportional is True, the actual width of the character will be used
            Note that in case of proportional, a blank will be 2 dots wide.

        narrow : bool
            if False (default), blanks will be 2 wide when proportional is True
            if True, blanks will be 1 wide when proportional is True

        Returns
        -------
        the number of dots of s : int

        """ 
        return len(self._str_to_pixel_lines(s, default=default, intra=intra, proportional=proportional, narrow=narrow)[0])

    def grid(self, s, default=" ", intra=1, proportional=False, width=None, align="c", narrow=False):
        """
        returns a list of boolean lists to represent the text s in the font

        Parameters
        ----------
        s : str
            string to represent

        default : str
            if a character has no representation in the font, it will be replaced
            with default, that is a blank by default
            if the length is not 1, a ValueError will be raised

        intra : int
            number of dots between characters
            default is 1

        proportional : bool
            if proportional is False (default), all characters will be 5 dots wide
            if proportional is True, the actual width of the character will be used
            Note that in case of proportional, a blank will be 2 dots wide.

        width : int
            width in dots of the result
            the default is the actal width (no align applied)
            if the actual width is smaller than width, the string will be padded according to the align parameter
            if the actual width is larger than width, the string is chopped according to the align parameter

        align : str
            if align starts with a c (default), the result will be centered
            if align starts with a l, the result will be left aligned
            if align starts with a r, the result will be right aligned

        narrow : bool
            if False (default), blanks will be 2 wide when proportional is True
            if True, blanks will be 1 wide when proportional is True

        Returns
        -------
        the representation of s : list of boolean lists
        each set dot will be True, not set False
        """
        if len(default) != 1:
            raise ValueError("len of default is not 1")

        pixel_lines = self._str_to_pixel_lines(s, default=default, intra=intra, proportional=proportional, narrow=narrow)

        if width is None:
            return pixel_lines
        actual_width = len(pixel_lines[0])
        extra = width - actual_width

        if extra >= 0:
            if align.lower().startswith("c"):
                extra_left = extra // 2
                extra_right = extra - extra_left
            elif align.lower().startswith("l"):
                extra_left = 0
                extra_right = extra
            elif align.lower().startswith("r"):
                extra_left = extra
                extra_right = 0
            else:
                raise ValueError("align does not start with c, l or r")

            return [extra_left * [False] + line + extra_right * [False] for line in pixel_lines]
        else:
            if align.lower().startswith("c"):
                start = -extra // 2
            elif align.lower().startswith("l"):
                start = 0
            elif align.lower().startswith("r"):
                start = -extra
            else:
                raise ValueError("align does not start with c, l or r")
            return [line[start : start + width] for line in pixel_lines]

    def coordinates(self, s, value=True, default=" ", intra=1, proportional=False, width=None, align="c", x_first=False, narrow=False, x_offset=0, y_offset=0):
        """
        returns a list of coordinates representing the text s in the font

        Parameters
        ----------
        s : str
            string to represent

        value : bool
            if True (default), the set dots will be returned
            if False, the non set dots will be returned

        default : str
            if a character has no representation in the font, it will be replaced
            with default, that is a blank by default
            if the length is not 1, a ValueError will be raised

        intra : int
            number of dots between characters
            default is 1

        proportional : bool
            if proportional is False (default), all characters will be 5 dots wide
            if proportional is True, the actual width of the character will be used
            Note that in case of proportional, a blank will be 2 dots wide.

        width : int
            width in dots of the result
            the default is the actal width (no align applied)
            if the actual width is smaller than width, the string will be padded according to the align parameter
            if the actual width is larger than width, the string is chopped according to the align parameter

        align : str
            if align starts with a c (default), the result will be centered
            if align starts with a l, the result will be left aligned
            if align starts with a r, the result will be right aligned

        x_first : bool
            if False (default), coordinates will be given row by row
            if True, coordinates will be given column by column

        narrow : bool
            if False (default), blanks will be 2 wide when proportional is True
            if True, blanks will be 1 wide when proportional is True

        x_offset : int
            adds this value to each of the x-coordinates (default 0)

        y_offset : int
            adds this value to each of the y-coordinates (default 0)

        Returns
        -------
        a list of coordinates (tuples) : list
        """
        result = []
        ct = self.grid(s, default=default, intra=intra, proportional=proportional, width=width, align=align, narrow=narrow)
        result = [(x + x_offset, y + y_offset) for y in range(self._height) for x, c in enumerate(ct[y]) if c == value]
        if x_first:
            result.sort()
        return result

    def grid_to_str(self, s, leftborder="<", rightborder=">", **kwargs):
        """
        returns a string representing the given string s, using * if a pixel is set.

        each line is prefixed with leftborder and postfixed with rightborder.
        all parameters for grid may be given as well
        """
        l = []
        for line in self.grid(s, **kwargs):
            l.append(leftborder + ("".join("*" if vl else " " for vl in line)) + rightborder)
        return "\n".join(l)

    def _check(self):
        for s in self._chartable:
            for i, c in enumerate(self._chartable[s]):
                if len(c) != self._width:
                    print(f"maybe error in {s} line {i}")
            if i != self._height - 1:
                print(f"error in {s} number of lines is {i+1}")


fiftydots = _Dots(
    height=10,
    width=5,
    name="fiftydots",
    spec="""
\x20
.....
.....
.....
.....
.....
.....
.....
.....
.....
.....
!
.....
..*..
..*..
..*..
..*..
..*..
.....
..*..
.....
.....
\x22
.....
.*.*.
.*.*.
.*.*.
.....
.....
.....
.....
.....
.....
#
.....
.*.*.
.*.*.
*****
.*.*.
*****
.*.*.
.*.*.
.....
.....
$
.....
..*..
.****
*.*..
.***.
..*.*
****.
..*..
.....
.....
%
.....
**...
**..*
...*.
..*..
.*...
*..**
...**
.....
.....
&
.....
.**..
*..*.
*.*..
.*...
*.*.*
*..*.
.**.*
.....
.....
\x27
.....
..*..
..*..
..*..
.....
.....
.....
.....
.....
.....
(
.....
...*.
..*..
.*...
.*...
.*...
..*..
...*.
.....
.....
)
.....
.*...
..*..
...*.
...*.
...*.
..*..
.*...
.....
.....
*
.....
.....
..*..
*.*.*
.***.
*.*.*
..*..
.....
.....
.....
+
.....
.....
..*..
..*..
*****
..*..
..*..
.....
.....
.....
,
.....
.....
.....
.....
.....
.....
..**.
..**.
...*.
..*..
-
.....
.....
.....
.....
*****
.....
.....
.....
.....
.....
.
.....
.....
.....
.....
.....
.....
..**.
..**.
.....
.....
/
.....
.....
....*
...*.
..*..
.*...
*....
.....
.....
.....
0
.....
.***.
*...*
*..**
*.*.*
**..*
*...*
.***.
.....
.....
1
.....
..*..
.**..
..*..
..*..
..*..
..*..
.***.
.....
.....
2
.....
.***.
*...*
....*
...*.
..*..
.*...
*****
.....
.....
3
.....
*****
...*.
..*..
...*.
....*
*...*
.***.
.....
.....
4
.....
...*.
..**.
.*.*.
*..*.
*****
...*.
...*.
.....
.....
5
.....
*****
*....
****.
....*
....*
*...*
.***.
.....
.....
6
.....
..**.
.*...
*....
****.
*...*
*...*
.***.
.....
.....
7
.....
*****
....*
...*.
..*..
..*..
..*..
..*..
.....
.....
8
.....
.***.
*...*
*...*
.***.
*...*
*...*
.***.
.....
.....
9
.....
.***.
*...*
*...*
.****
....*
...*.
.**..
.....
.....
;
.....
.....
.....
..**.
..**.
.....
..**.
..**.
...*.
..*..
:
.....
.....
.....
..**.
..**.
.....
..**.
..**.
.....
.....
<
.....
....*
...*.
..*..
.*...
..*..
...*.
....*
.....
.....
=
.....
.....
.....
*****
.....
*****
.....
.....
.....
.....
>
.....
*....
.*...
..*..
...*.
..*..
.*...
*....
.....
.....
?
.....
.***.
*...*
....*
...*.
..*..
.....
..*..
.....
.....
@
.....
.***.
*...*
....*
.*..*
*.*.*
*.*.*
.***.
.....
.....
A
.....
.***.
*...*
*...*
*****
*...*
*...*
*...*
.....
.....
B
.....
****.
*...*
*...*
****.
*...*
*...*
****.
.....
.....
C
.....
.***.
*...*
*....
*....
*....
*...*
.***.
.....
.....
D
.....
***..
*..*.
*...*
*...*
*...*
*..*.
***..
.....
.....
E
.....
*****
*....
*....
****.
*....
*....
*****
.....
.....
F
.....
*****
*....
*....
****.
*....
*....
*....
.....
.....
G
.....
.***.
*...*
*....
*.***
*...*
*...*
.****
.....
.....
H
.....
*...*
*...*
*...*
*****
*...*
*...*
*...*
.....
.....
I
.....
.***.
..*..
..*..
..*..
..*..
..*..
.***.
.....
.....
J
.....
..***
...*.
...*.
...*.
...*.
*..*.
.**..
.....
.....
K
.....
*...*
*..*.
*.*..
**...
*.*..
*..*.
*...*
.....
.....
L
.....
*....
*....
*....
*....
*....
*....
*****
.....
.....
M
.....
*...*
**.**
*.*.*
*...*
*...*
*...*
*...*
.....
.....
N
.....
*...*
*...*
**..*
*.*.*
*..**
*...*
*...*
.....
.....
O
.....
.***.
*...*
*...*
*...*
*...*
*...*
.***.
.....
.....
P
.....
****.
*...*
*...*
****.
*....
*....
*....
.....
.....
Q
.....
.***.
*...*
*...*
*...*
*.*.*
*..*.
.**.*
.....
.....
R
.....
****.
*...*
*...*
****.
*.*..
*..*.
*...*
.....
.....
S
.....
.***.
*...*
*....
.***.
....*
*...*
.***.
.....
.....
T
.....
*****
..*..
..*..
..*..
..*..
..*..
..*..
.....
.....
U
.....
*...*
*...*
*...*
*...*
*...*
*...*
.***.
.....
.....
V
.....
*...*
*...*
*...*
*...*
*...*
.*.*.
..*..
.....
.....
W
.....
*...*
*...*
*...*
*.*.*
*.*.*
**.**
*...*
.....
.....
X
.....
*...*
*...*
.*.*.
..*..
.*.*.
*...*
*...*
.....
.....
Y
.....
*...*
*...*
.*.*.
..*..
..*..
..*..
..*..
.....
.....
Z
.....
*****
....*
...*.
..*..
.*...
*....
*****
.....
.....
[
.....
.***.
.*...
.*...
.*...
.*...
.*...
.***.
.....
.....
\x5c
.....
.....
*....
.*...
..*..
...*.
....*
.....
.....
.....
]
.....
.***.
...*.
...*.
...*.
...*.
...*.
.***.
.....
.....
^
.....
..*..
.*.*.
*...*
.....
.....
.....
.....
.....
.....
_
.....
.....
.....
.....
.....
.....
.....
*****
.....
.....
`
.....
.*...
..*..
...*.
.....
.....
.....
.....
.....
.....
a
.....
.....
.....
.***.
....*
.****
*...*
.****
.....
.....
b
.....
*....
*....
*.**.
**..*
*...*
*...*
.***.
.....
.....
c
.....
.....
.....
.***.
*....
*....
*...*
.***.
.....
.....
d
.....
....*
....*
.**.*
*..**
*...*
*...*
.****
.....
.....
e
.....
.....
.....
.***.
*...*
*****
*....
.***.
.....
.....
f
.....
...*.
..*.*
..*..
.***.
..*..
..*..
..*..
.....
.....
g
.....
.....
.....
.****
*...*
*...*
*..**
.**.*
....*
.***.
h
.....
*....
*....
*.**.
**..*
*...*
*...*
*...*
.....
.....
i
.....
..*..
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
j
.....
...*.
.....
..**.
...*.
...*.
...*.
...*.
*..*.
.**..
k
.....
.*...
.*...
.*..*
.*.*.
.**..
.*.*.
.*..*
.....
.....
l
.....
.**..
..*..
..*..
..*..
..*..
..*..
.***.
.....
.....
m
.....
.....
.....
**.*.
*.*.*
*.*.*
*.*.*
*.*.*
.....
.....
n
.....
.....
.....
*.**.
**..*
*...*
*...*
*...*
.....
.....
o
.....
.....
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
p
.....
.....
.....
*.**.
**..*
*...*
**..*
*.**.
*....
*....
q
.....
.....
.....
.**.*
*..**
*...*
*..**
.**.*
....*
....*
r
.....
.....
.....
.*.**
.**..
.*...
.*...
.*...
.....
.....
s
.....
.....
.....
.****
*....
.***.
....*
****.
.....
.....
t
.....
..*..
..*..
.***.
..*..
..*..
..*.*
...*.
.....
.....
u
.....
.....
.....
*...*
*...*
*...*
*..**
.**.*
.....
.....
v
.....
.....
.....
*...*
*...*
*...*
.*.*.
..*..
.....
.....
w
.....
.....
.....
*...*
*...*
*.*.*
*.*.*
.*.*.
.....
.....
x
.....
.....
.....
*...*
.*.*.
..*..
.*.*.
*...*
.....
.....
y
.....
.....
.....
*...*
*...*
*...*
*..**
.**.*
....*
.***.
z
.....
.....
.....
*****
...*.
..*..
.*...
*****
.....
.....
{
.....
...**
..*..
..*..
.*...
..*..
..*..
...**
.....
.....
|
.....
..*..
..*..
..*..
..*..
..*..
..*..
..*..
.....
.....
}
.....
**...
..*..
..*..
...*.
..*..
..*..
**...
.....
.....
~
.....
.*...
*.*.*
...*.
.....
.....
.....
.....
.....
.....
\x7f
.....
*.*.*
.*.*.
*.*.*
.*.*.
*.*.*
.*.*.
*.*.*
.....
.....
ä
.....
.*.*.
.....
.***.
....*
.****
*...*
.****
.....
.....
à
.*...
..*..
.....
.***.
....*
.****
*...*
.****
.....
.....
á
...*.
..*..
.....
.***.
....*
.****
*...*
.****
.....
.....
â
..*..
.*.*.
.....
.***.
....*
.****
*...*
.****
.....
.....
å
..*..
.*.*.
..*..
.***.
....*
.****
*...*
.****
.....
.....
ã
.*...
*.*.*
...*.
.***.
....*
.****
*...*
.****
.....
.....
æ
.....
.....
.....
**.*.
..*.*
.****
*.*..
.*.**
.....
.....
Ä
.....
.*.*.
.....
.***.
*...*
*****
*...*
*...*
.....
.....
À
.*...
..*..
.....
.***.
*...*
*****
*...*
*...*
.....
.....
Á
...*.
..*..
.....
.***.
*...*
*****
*...*
*...*
.....
.....
Â
..*..
.*.*.
.....
.***.
*...*
*****
*...*
*...*
.....
.....
Å
..*..
.*.*.
..*..
.***.
*...*
*****
*...*
*...*
.....
.....
Ã
.*...
*.*.*
...*.
.***.
*...*
*****
*...*
*...*
.....
.....
Æ
.....
.****
*.*..
*.*..
*****
*.*..
*.*..
*.***
.....
.....
ë
.....
.*.*.
.....
.***.
*...*
*****
*....
.***.
.....
.....
è
.*...
..*..
.....
.***.
*...*
*****
*....
.***.
.....
.....
é
...*.
..*..
.....
.***.
*...*
*****
*....
.***.
.....
.....
ê
..*..
.*.*.
.....
.***.
*...*
*****
*....
.***.
.....
.....
Ë
.....
.*.*.
.....
*****
*....
****.
*....
*****
.....
.....
È
.*...
..*..
.....
*****
*....
****.
*....
*****
.....
.....
É
...*.
..*..
.....
*****
*....
****.
*....
*****
.....
.....
Ê
..*..
.*.*.
.....
*****
*....
****.
*....
*****
.....
.....
ï
.....
.*.*.
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
ì
.*...
..*..
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
í
...*.
..*..
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
î
..*..
.*.*.
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
Ï
.....
.*.*.
.....
.***.
..*..
..*..
..*..
.***.
.....
.....
Ì
.*...
..*..
.....
.***.
..*..
..*..
..*..
.***.
.....
.....
Í
...*.
..*..
.....
.***.
..*..
..*..
..*..
.***.
.....
.....
Î
..*..
.*.*.
.....
.***.
..*..
..*..
..*..
.***.
.....
.....
ö
.....
.*.*.
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
ò
.*...
..*..
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
ó
...*.
..*..
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
ô
..*..
.*.*.
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
õ
.*...
*.*.*
...*.
.***.
*...*
*...*
*...*
.***.
.....
.....
ø
.....
.....
.....
.***.
*..**
*.*.*
**..*
.***.
.....
.....
œ
.....
.....
.....
.*.*.
*.*.*
*.***
*.*..
.*.**
.....
.....
Ö
.....
.*.*.
.....
*****
*...*
*...*
*...*
*****
.....
.....
Ò
.*...
..*..
.....
*****
*...*
*...*
*...*
*****
.....
.....
Ó
...*.
..*..
.....
*****
*...*
*...*
*...*
*****
.....
.....
Ô
..*..
.*.*.
.....
*****
*...*
*...*
*...*
*****
.....
.....
Õ
.*...
*.*.*
...*.
*****
*...*
*...*
*...*
*****
.....
.....
Ø
.....
.....
.....
*****
*..**
*.*.*
**..*
*****
.....
.....
Œ
.....
.****
*.*..
*.*..
*.***
*.*..
*.*..
.****
.....
.....
ü
.....
.*.*.
.....
*...*
*...*
*...*
*..**
.**.*
.....
.....
ù
.*...
..*..
.....
*...*
*...*
*...*
*..**
.**.*
.....
.....
ú
...*.
..*..
.....
*...*
*...*
*...*
*..**
.**.*
.....
.....
û
..*..
.*.*.
.....
*...*
*...*
*...*
*..**
.**.*
.....
.....
Ü
.....
.*.*.
.....
*...*
*...*
*...*
*...*
.***.
.....
.....
Ù
.*...
..*..
.....
*...*
*...*
*...*
*...*
.***.
.....
.....
Ú
...*.
..*..
.....
*...*
*...*
*...*
*...*
.***.
.....
.....
Û
..*..
.*.*.
.....
*...*
*...*
*...*
*...*
.***.
.....
.....
ñ
.*...
*.*.*
...*.
*.**.
**..*
*...*
*...*
*...*
.....
.....
ĳ
.....
.*..*
.....
.*..*
.*..*
.*..*
.*..*
.*..*
....*
.***.
Ĳ
.....
.*..*
.*..*
.*..*
.*..*
....*
....*
.***.
.....
.....
ç
.....
.....
.....
.***.
*....
*....
*...*
.***.
...*.
..**.
ý
...*.
..*..
.....
*...*
*...*
*...*
*..**
.**.*
....*
.***.
ć
.....
...*.
..*..
.***.
*....
*....
*...*
.***.
.....
.....
č
.....
.*.*.
..*..
.***.
*....
*....
*...*
.***.
.....
.....
ę
.....
.....
.....
.***.
*...*
*****
*....
.***.
..*..
..**.
ī
.....
.***.
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
ı
.....
.....
.....
.**..
..*..
..*..
..*..
.***.
.....
.....
ś
.....
...*.
..*..
.****
*....
.***.
....*
****.
.....
.....
Š
.....
...*.
..*..
*****
*....
*****
....*
*****
.....
.....
ť
.....
..*.*
..**.
.***.
..*..
..*..
..*.*
...*.
.....
.....
ų
.....
.....
.....
*...*
*...*
*...*
*...*
.***.
...*.
...**
Κ
.....
*...*
*..*.
*.*..
**...
*.*..
*..*.
*...*
.....
.....
ά
..*..
.*...
.....
.*.*.
*.*..
*..*.
*.*..
.*.*.
.....
.....
ή
...*.
..*..
.....
*.**.
**..*
*...*
*...*
*...*
....*
....*
α
.....
.....
.....
.*.*.
*.*..
*..*.
*.*..
.*.*.
.....
.....
ι
.....
.....
.....
.**..
..*..
..*..
..*..
...*.
.....
.....
λ
.....
*....
.*...
..*..
..**.
.*..*
*...*
*...*
.....
.....
ν
.....
.....
.....
*...*
*...*
*...*
*..*.
.**..
.....
.....
ο
.....
.....
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
ρ
.....
.....
.....
.***.
*...*
*...*
*...*
****.
*....
*....
χ
.....
.....
.....
**..*
.*..*
..**.
.**..
.*.*.
*..*.
*..**
Г
.....
*****
*....
*....
*....
*....
*....
*....
.....
.....
З
.....
.**..
*..*.
....*
..**.
....*
*...*
.***.
.....
.....
Н
.....
*...*
*...*
*...*
*****
*...*
*...*
*...*
.....
.....
С
.....
.***.
*...*
*....
*....
*....
*...*
.***.
.....
.....
Ч
.....
*...*
*...*
*...*
*...*
.**.*
....*
....*
.....
.....
а
.....
.....
.....
.***.
....*
.****
*...*
.****
.....
.....
в
.....
.....
.....
****.
*...*
****.
*...*
****.
.....
.....
г
.....
.....
.....
*****
*....
*....
*....
*....
.....
.....
д
.....
.....
.....
.***.
.* *.
.*.*.
.*.*.
*****
*...*
.....
е
.....
.....
.....
.***.
*...*
*****
*....
.***.
.....
.....
и
.....
.....
.....
*...*
*..**
*.*.*
**..*
*...*
.....
.....
к
.....
.....
.....
*..*.
*.*..
**...
*.*..
*..*.
.....
.....
м
.....
.....
.....
*...*
**.**
*.*.*
*...*
*...*
.....
.....
н
.....
.....
.....
*...*
*...*
*****
*...*
*...*
.....
.....
о
.....
.....
.....
.***.
*...*
*...*
*...*
.***.
.....
.....
р
.....
.....
.....
*.**.
**..*
*...*
**..*
*.**.
*....
*....
с
.....
.....
.....
.***.
*....
*....
*...*
.***.
.....
.....
т
.....
.....
.....
*****
..*..
..*..
..*..
..*..
.....
.....
ы
.....
.....
.....
*...*
*...*
**..*
*.*.*
**..*
.....
.....
ќ
..*..
.*...
.....
*..*.
*.*..
**...
*.*..
*..*.
.....
.....
\u1492
.....
.....
****.
....*
*...*
*...*
*...*
*...*
.....
.....
\u1489
.....
.....
***..
...*.
...*.
...*.
...*.
*****
.....
.....
\u1493
.....
.....
..*..
..*..
..*..
..*..
..*..
..*..
.....
.....
\u1496
.....
.....
*..**
*.*.*
*...*
*...*
*...*
.***.
.....
.....
\u1504
.....
.....
.**,.
...*.
...*.
...*.
...*.
.***.
.....
.....
\u1513
.....
.....
*.*.*
*.*.*
*.*.*
**..*
*...*
.***.
.....
.....
""",
)

fifteendots = _Dots(
    height=5,
    width=3,
    name="fifteendots",
    spec="""
\x20
...
...
...
...
...
.
...
...
...
...
.*.
,
...
...
...
**.
.*.
:
...
.*.
...
.*.
...
=
...
***
...
***
...
-
...
...
***
...
...
0
***
*.*
*.*
*.*
***
1
.*.
**.
.*.
.*.
***
2
***
..*
***
*..
***
3
***
..*
***
..*
***
4
*.*
*.*
***
..*
..*
5
***
*..
***
..*
***
6
***
*..
***
*.*
***
7
***
..*
.*.
.*.
.*.
8
***
*.*
***
*.*
***
9
***
*.*
***
..*
***
a
...
.**
*.*
*.*
***
b
*..
***
*.*
*.*
***
c
...
***
*..
*..
***
d
..*
***
*.*
*.*
***
e
...
.**
*.*
**.
.**
f
.**
.*.
***
.*.
.*.
g
...
***
*..
*.*
***
h
*..
***
*.*
*.*
*.*
i
...
.*.
.*.
.*.
.*.
j
...
.*.
.*.
.*.
**.
k
...
*.*
**.
*.*
*.*
l
...
*..
*..
*..
**.
m
...
*.*
***
*.*
*.*
n
...
***
*.*
*.*
*.*
o
...
***
*.*
*.*
***
p
...
***
*.*
***
*..
q
...
***
*.*
***
..*
r
...
***
*..
*..
*..
s
...
.**
.*.
.*.
**.
t
.*.
***
.*.
.*.
.*.
u
...
*.*
*.*
*.*
***
v
...
*.*
*.*
**.
*..
w
...
*.*
*.*
***
*.*
x
...
*.*
.*.
.*.
*.*
y
...
*.*
***
..*
***
z
...
***
..*
.*.
***
A
***
*.*
***
*.*
*.*
B
**.
*.*
***
*.*
**.
C
***
*..
*..
*..
***
D
**.
*.*
*.*
*.*
**.
E
***
*..
***
*..
***
F
***
*..
***
*..
*..
G
***
*..
*.*
*.*
***
H
*.*
*.*
***
*.*
*.*
I
***
.*.
.*.
.*.
***
J
..*
..*
..*
..*
***
K
*.*
*.*
**.
*.*
*.*
L
*..
*..
*..
*..
***
M
*.*
***
***
*.*
*.*
N
***
*.*
*.*
*.*
*.*
O
.*.
*.*
*.*
*.*
.*.
P
***
*.*
***
*..
*..
Q
***
*.*
***
..*
..*
R
***
*.*
**.
*.*
*.*
S
.**
*..
.*.
..*
**.
T
***
.*.
.*.
.*.
.*.
U
*.*
*.*
*.*
*.*
***
V
*.*
*.*
*.*
**.
*..
W
*.*
*.*
***
***
*.*
X
*.*
*.*
.*.
*.*
*.*
Y
*.*
*.*
***
..*
***
Z
***
..*
.*.
*..
***
\x7f
*.*
.*.
*.*
.*.
*.*
""",
)

twentyfourdots = _Dots(
    height=8,
    width=3,
    name="twentyfourdots",
    spec="""
\x20
...
...
...
...
...
...
...
...
.
...
...
...
...
...
...
*..
...
,
...
...
...
...
...
.*.
.*.
*..
%
...
*.*
..*
.*.
*..
*.*
...
...
:
...
...
.*.
...
.*.
...
...
...
-
...
...
...
**.
...
...
...
...
=
...
...
***
...
***
...
...
...
0
***
*.*
*.*
*.*
*.*
*.*
***
...
1
.*.
**.
.*.
.*.
.*.
.*.
***
...
2
***
..*
..*
***
*..
*..
***
...
3
***
..*
..*
***
..*
..*
***
...
4
*.*
*.*
*.*
***
..*
..*
..*
...
5
***
*..
*..
***
..*
..*
***
...
6
***
*..
*..
***
*.*
*.*
***
...
7
***
..*
..*
.*.
.*.
.*.
.*.
...
8
***
*.*
*.*
***
*.*
*.*
***
...
9
***
*.*
*.*
***
..*
..*
***
...
a
...
...
***
..*
***
*.*
***
...
b
*..
*..
***
*.*
*.*
*.*
***
...
c
...
...
***
*..
*..
*..
***
...
d
..*
..*
***
*.*
*.*
*.*
***
...
e
...
...
***
*.*
***
*..
***
...
f
.**
.*.
***
.*.
.*.
.*.
.*.
...
g
...
...
***
*.*
*.*
***
..*
***
h
*..
*..
***
*.*
*.*
*.*
* *
...
i
.*.
...
.*.
.*.
.*.
.*.
 *.
...
j
.*.
...
**.
.*.
.*.
.*.
 *.
*..
k
*..
*..
*.*
**.
*..
**.
* *
...
l
*..
*..
*..
*..
*..
*..
**.
...
m
...
...
*.*
***
*.*
*.*
*.*
...
n
...
...
**.
*.*
*.*
*.*
*.*
...
o
...
...
***
*.*
*.*
*.*
***
...
p
...
...
***
*.*
*.*
***
*..
*..
q
...
...
***
*.*
*.*
*.*
***
..*
r
...
...
***
*..
*..
*..
*..
...
s
...
...
***
*..
***
..*
***
...
t
*..
*..
***
*..
*..
*..
***
...
u
...
...
*.*
*.*
*.*
*.*
***
...
v
...
...
*.*
*.*
*.*
*.*
.*.
...
w
...
...
*.*
*.*
*.*
***
*.*
...
x
...
...
*.*
*.*
.*.
*.*
*.*
...
y
...
...
*.*
*.*
*.*
***
..*
**.
z
...
...
***
..*
.*.
*..
***
...
A
.*.
*.*
*.*
***
*.*
*.*
*.*
...
B
**.
*.*
*.*
**.
*.*
*.*
**.
...
C
.**
*..
*..
*..
*..
*..
.**
...
D
**.
*.*
*.*
*.*
*.*
*.*
**.
...
E
***
*..
*..
***
*..
*..
***
...
F
***
*..
*..
***
*..
*..
*..
...
G
.*.
*.*
*..
*.*
*.*
*.*
.*.
...
H
*.*
*.*
*.*
***
*.*
*.*
*.*
...
I
***
.*.
.*.
.*.
.*.
.*.
***
...
J
..*
..*
..*
..*
..*
*.*
.*.
...
K
*.*
*.*
**.
*..
**.
*.*
*.*
...
L
*..
*..
*..
*..
*..
*..
***
...
M
*.*
***
***
*.*
*.*
*.*
*.*
...
N
**.
*.*
*.*
*.*
*.*
*.*
*.*
...
O
.*.
*.*
*.*
*.*
*.*
*.*
.*.
...
P
***
*.*
*.*
***
*..
*..
*..
...
Q
.*.
*.*
*.*
*.*
*.*
.*.
..*
...
R
**'
*.*
*.*
**.
*.*
*.*
*.*
...
S
.**
*..
*..
.*.
..*
..*
**.
...
T
***
 *.
.*.
.*.
.*.
.*.
.*.
...
U
*.*
*.*
*.*
*.*
*.*
*.*
***
...
V
*.*
*.*
*.*
*.*
*.*
*.*
.*.
...
W
*.*
*.*
*.*
*.*
***
***
*.*
...
X
*.*
*.*
*.*
.*.
*.*
*.*
*.*
...
Y
*.*
*.*
*.*
*.*
.*.
.*.
.*.
...
Z
***
..*
..*
.*.
*..
*..
***
...
|
.*.
.*.
.*.
.*.
.*.
.*.
.*.
...
\x7f
*.*
.*.
*.*
.*.
*.*
.*.
*.*
.*.
""",
)


if __name__ == "__main__":
    print(twentyfourdots.number_of_pixels("mwGMW", intra=2, proportional=False))
    twentyfourdots._check()
    print(twentyfourdots.coordinates("ab"))
    print(twentyfourdots.grid_to_str("ij mwGMW", intra=2, proportional=False, width=None, align="c"))
    print(twentyfourdots.grid_to_str("ij mwGMW", intra=2, proportional=True, width=None, align="c"))


#    print(fiftydots.grid_to_str("abcdefghijklmnopqrstuvwxyz", intra=1, proportional=False, width=None, align="c"))

# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=False, width=80, align="c")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=False, width=80, align="l")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=False, width=80, align="r")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=False, width=40, align="c")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=False, width=40, align="l")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=False, width=40, align="r")))

# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=None, align="c")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=80, align="c")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=80, align="l")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=80, align="r")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=40, align="c")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=40, align="l")))
# print(grid_to_str(grid("abc defghi!A", intra=1, proportional=True, width=40, align="r")))

# print(coordinates("a"))

# print(coordinates("a", x_first=True))
