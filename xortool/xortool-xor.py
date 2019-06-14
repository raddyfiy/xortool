#! python2
#-*- coding:utf-8 -*-

"""
xor strings
options:
    -s  -  string with \\xAF escapes
    -r  -  raw string
    -h  -  hex-encoded string (non-letterdigit chars are stripped)
    -f  -  read data from file (- for stdin)
    -n  -  no newline at the end(you'd better add -n to keep file original)
    -o  -  outfile name(This is different from linux version,do not use > to save file)


    --no-cycle / --nc  -  pad smaller strings with null bytes
example: python xortool-xor.py -f ./text/cmd.exe -s "secret_key" -n -o binary_xored_cmd

author: hellman ( hellman1908@gmail.com )
"""

from __future__ import print_function
import sys
import string
import getopt

DATA_OPTS = "s:r:h:f:o:"
HEXES = set("0123456789abcdefABCDEF")

def main():
    nocycle = False
    nonewline = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n" + DATA_OPTS, ["no-cycle", "nc"])
        datas = []
        for c, val in opts:
            if c =="-o":
                outfilename=val
                continue
            if c in ("--no-cycle", "--nc"):
                nocycle = True
            elif c == "-n":
                nonewline = True
            else:
                v = arg_data(c, val)
                if v is None:
                    raise getopt.GetoptError("unknown option %s" % c)
                datas.append(v)
        if not datas:
            raise getopt.GetoptError("no data given")
    except getopt.GetoptError as e:
        print("error:", e, file=sys.stderr)
        print(__doc__, file=sys.stderr)
        quit()

    outfile=open(outfilename,'wb')

    outfile.write(xor(datas, nocycle=nocycle))
    if not nonewline:
        outfile.write("\n")

    outfile.close()


def xor(args, nocycle=False):
    maxlen = max(map(len, args))
    res = [0] * maxlen
    if nocycle:
        for s in args:
            for i in xrange(len(s)):
                res[i] ^= ord(s[i])
    else:
        for s in args:
            slen = len(s)
            for i in xrange(maxlen):
                res[i] ^= ord(s[i % slen])
    return "".join(map(chr, res))


def from_str(s):
    res = ""
    i = 0
    while True:
        if i + 4 > len(s):
            break

        if s[i+1] == "x" and s[i+2] in HEXES and s[i+3] in HEXES:
            res += chr(int(s[i+2:i+4], 16))
            i += 4
        else:
            res += s[i]
            i += 1
    res += s[i:]
    return res

def from_hex(s):
    res = ""
    for c in s:
        if c in HEXES:
            res += c
        elif c in string.ascii_letters:
            raise ValueError("Bad splitters (alphanum)")
    return res.decode("hex")

def from_file(s):
    if s == "-":
        return sys.stdin.read()
    return open(s, "rb").read()

def arg_data(opt, s):
    if opt == "-s":
        return from_str(s)
    elif opt == "-r":
        return s
    elif opt == "-h":
        return from_hex(s)
    elif opt == "-f":
        return from_file(s)
    return None


if __name__ == '__main__':
    main()
