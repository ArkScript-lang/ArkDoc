# ArkDoc ![release](https://img.shields.io/github/v/release/ArkScript-lang/ArkDoc)

It's a **Lite** documentation generator for arkscript based on Mkdocs, and written in ruby.

![licence](https://img.shields.io/badge/licence-MPL%202.0-2)
![code size](https://img.shields.io/github/languages/code-size/ArkScript-lang/ArkDoc)

## Dependencies

* Python >= 2.7 (Python 3.7 tested and working)
* Ruby >= 2.5

## Usage

```bash
# Clone repository
~$ git clone https://github.com/ArkScript-lang/ArkDoc.git
# The documentation will be generated in this folder
~/ArkDoc$ mkdir docs
# Put your arkscript files in this folder (default source directory)
# you can change it with -S option
~/ArkDoc$ mkdir ark
# Install Mkdocs
~$ pip install mkdocs
# Print help
~/ArkDoc$ ruby ArkDoc.rb -H
# Build site in docs/[SITE_NAME]/site with default source directory
~/ArkDoc$ ruby ArkDoc.rb --G [SITE_NAME]
```

You cand find the syntax ![here](./Syntax.md).

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
