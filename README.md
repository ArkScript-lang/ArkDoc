# ArkDoc ![release](https://img.shields.io/github/v/release/ArkScript-lang/ArkDoc)

It's a **Lite** documentation generator for arkscript based on Mkdocs, and written in ruby.

![licence](https://img.shields.io/badge/licence-MPL%202.0-2)
![code size](https://img.shields.io/github/languages/code-size/ArkScript-lang/ArkDoc)
![Ruby CI](https://github.com/ArkScript-lang/ArkDoc/workflows/Ruby%20CI/badge.svg)

## Dependencies

* Python >= 2.7 (Python 3.7 tested and working)
* Ruby >= 2.5

## Usage

```bash
# first, clone repository
~$ git clone https://github.com/ArkScript-lang/ArkDoc.git
~$ cd ArkDoc
# put your arkscript files in this folder (default source directory)
# you can change it with -s option
~/ArkDoc$ mkdir source
# install Mkdocs
~$ pip install mkdocs
# running
~/ArkDoc$ ruby ArkDoc.rb --help
DESCRIPTION
      	Lite documentation generator based on Mkdocs

SYNOPSIS
        ruby ArkDoc.rb -h
        ruby ArkDoc.rb -v
        ruby ArkDoc.rb -g <site name> [-s <source path>]
        ruby ArkDoc.rb -md <site name> [-s <source path>]

OPTIONS
        -h, --help              Print this help message
        -v, --version           Print ArkDoc version and exit
        -g, --generate          Generate the website and exit
        -md, --markdown         Generate the markdown files and exit
        -s, --source            Set the path of souree files directory

LICENCE
        Mozilla Public License 2.0
```

## Syntax
You can be find the syntax ![here](./Syntax.md).

## Example
```clojure
###
# @brief Reverse a string.
# @param _string the string to reverse
# @details The original string is left unmodified.
# =begin
# (import "String.ark")
# (let message "hello world, I like goats")
# (let reversed (str:reverse message))  # => staog ekil I ,dlrow olleh
# =end
# @author https://github.com/Natendrtfm
##
(let str:reverse (fun (_string) {
    (mut _index (- (len _string) 1))
    (mut _returnedString "")
    (while (> _index -1) {
        (set _returnedString (+ _returnedString (@ _string _index)))
        (set _index (- _index 1))
    })
    _returnedString
}))
```

![string](./images/example.png)