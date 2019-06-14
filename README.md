xortool.py for windows
====================

A tool to do some xor analysis:

  - guess the key length (based on count of equal chars)
  - guess the key (base on knowledge of most frequent char)

need python2
note: some commands are different from linux version 
-----------
Usage


```
xortool
  A tool to do some xor analysis:
  - guess the key length (based on count of equal chars)
  - guess the key (base on knowledge of most frequent char)

Usage:
  python xortool.py [-x] [-m MAX-LEN] [-f] [-t CHARSET] [FILE]
  python xortool.py [-x] [-l LEN] [-c CHAR | -b | -o] [-f] [-t CHARSET] [FILE]
  python xortool.py [-x] [-m MAX-LEN| -l LEN] [-c CHAR | -b | -o] [-f] [-t CHARSET] [FILE]
  python xortool.py [-h | --help]
  python xortool.py --version

Options:
  -x --hex                          input is hex-encoded str
  -l LEN, --key-length=LEN          length of the key
  -m MAX-LEN, --max-keylen=MAX-LEN  maximum key length to probe [default: 65]
  -c CHAR, --char=CHAR              most frequent char (one char or hex code)
  -b --brute-chars                  brute force all possible most frequent chars
  -o --brute-printable              same as -b but will only check printable chars
  -f --filter-output                filter outputs based on the charset
  -t CHARSET --text-charset=CHARSET target text character set [default: printable]
  -h --help                         show this help

Notes:
  Text character set:
    * Pre-defined sets: printable, base32, base64
    * Custom sets:
      - a: lowercase chars
      - A: uppercase chars
      - 1: digits
      - !: special chars
      - *: printable chars

Examples:
  python xortool.py file.bin
  python xortool.py -l 11 -c 20 file.bin
  python xortool.py -x -c ' ' file.hex
  python xortool.py -b -f -l 23 -t base64 message.enc
```

Example 1
---------------------

```cmd
D:\xortool> python xortool-xor.py -f ./text/cmd.exe -s "secret_key" -n -o binary_xored_cmd

*This is different from linux version,do not use > to save file*
*To remain file unchanged, you'd better add -n. Most scenes need -n*


D:\xortool> python xortool.py binary_xored_cmd
The most probable key lengths:
   1:   9.3%
   5:   15.2%
  10:   21.6%
  15:   9.4%
  20:   13.5%
  25:   6.1%
  30:   9.1%
  35:   4.2%
  40:   6.6%
  50:   5.0%
Key-length can be 5*n
Most possible char is needed to guess the key!

# 00 is the most frequent byte in binaries
D:\xortool> python xortool.py binary_xored_cmd -l 10 -c 00
...
1 possible key(s) of length 10:
secret_key

# decrypted ciphertexts are placed in ./xortool_out/Number_<key repr>
# ( have no better idea )
D:\xortool >certutil -hashfile text/cmd.exe MD5
MD5 哈希(文件 text/cmd.exe):
a6 17 7d 08 07 59 cf 4a 03 ef 83 7a 38 f6 24 01

D:\xortool >certutil -hashfile xortool_out/0.out MD5
MD5 哈希(文件 xortool_out/0.out):
a6 17 7d 08 07 59 cf 4a 03 ef 83 7a 38 f6 24 01
```

The most common use is to pass just the encrypted file and the most frequent character (usually 00 for binaries and 20 for text files) - length will be automatically chosen:

```bash
D:\xortool> python xortool.py tool_xored -c 20
The most probable key lengths:
   2:   10.4%
   5:   13.0%
   8:   8.8%
  10:   15.7%
  12:   6.9%
  15:   8.1%
  20:   16.9%
  25:   5.4%
  30:   6.6%
  40:   8.1%
Key-length can be 5*n
1 possible key(s) of length 20:
an0ther s3cret \xdd key
```

Here, the key is longer then default 32 limit:

```bash
D:\xortool> python xortool.py ls_xored -c 00 -m 64
The most probable key lengths:
   1:   9.3%
   3:   11.2%
   6:   9.9%
   9:   8.6%
  11:   16.5%
  15:   6.4%
  18:   5.6%
  22:   10.0%
  33:   17.9%
  44:   4.8%
Key-length can be 3*n
1 possible key(s) of length 33:
really long s3cr3t k3y... PADDING
```

So, if automated decryption fails, you can calibrate:

- (`-m`) max length to try longer keys
- (`-l`) selected length to see some interesting keys
- (`-c`) the most frequent char to produce right plaintext

Example 2
---------------------

We are given a message in encoded in Base64 and XORed with an unknown key.

```bash
D:\xortool> python xortool.py message.enc 
The most probable key lengths:
   2:   12.3%
   4:   13.8%
   6:   10.5%
   8:   11.5%
  10:   8.6%
  12:   9.4%
  14:   7.1%
  16:   7.8%
  23:   10.4%
  46:   8.7%
Key-length can be 4*n
Most possible char is needed to guess the key!
```

We can now test the key lengths while filtering the outputs so that it only keeps the plaintexts holding the character set of Base64. After trying a few lengths, we come to the right one, which gives only 1 plaintext with a percentage of valid characters above the default threshold of 95%.

```bash
D:\xortool> python xortool.py message.enc -b -f -l 23 -t base64
256 possible key(s) of length 23:
\x01=\x121#"0\x17\x13\t\x7f ,&/\x12s\x114u\x170#
\x00<\x130"#1\x16\x12\x08~!-\'.\x13r\x105t\x161"
\x03?\x103! 2\x15\x11\x0b}".$-\x10q\x136w\x152!
\x02>\x112 !3\x14\x10\n|#/%,\x11p\x127v\x143 
\x059\x165\'&4\x13\x17\r{$("+\x16w\x150q\x134\'
...
Found 1 plaintexts with 95.0%+ valid characters
See files filename-key.csv, filename-char_used-perc_valid.csv
```

By filtering the outputs on the character set of Base64, we directly keep the only solution.

Information
---------------------

Author: hellman ( hellman1908@gmail.com )

windows version: (fiy.sheng11@gmail.com)

License: MIT License (opensource.org/licenses/MIT)
