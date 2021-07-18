# ArkDoc ![release](https://img.shields.io/github/v/release/ArkScript-lang/ArkDoc)

![licence](https://img.shields.io/badge/licence-MPL%202.0-2)
![code size](https://img.shields.io/github/languages/code-size/ArkScript-lang/ArkDoc)

A documentation generator for ArkScript.

## Dependencies

* Python >= 3.9

## Usage

```bash
git clone https://github.com/ArkScript-lang/ArkDoc.git
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 -m arkdoc --help
```

## Syntax

- `@meta <name>`
- `@brief <description>`
- `@param <name> <description>`
- `@details <description>`
- `=begin` / code block / `=end`
- `@author <url>,<url>,...`

## Example

```lisp
# @meta List
# @brief Iterate over a given list and run a given function on every element.
# @param _L the list to iterate over
# @param _func the function to call on each element
# @details The original list is left unmodified.
# =begin
# (import "List.ark")
# (let collection [1 2 5 12])
# (list:forEach collection (fun (element) {
#     (print element)
# }))
# =end
# @author https://github.com/SuperFola
(let list:forEach (fun (_L _func) {
    (mut _index 0)
    (while (< _index (len _L)) {
        (mut _element (@ _L _index))
        (_func _element)
        (set _index (+ 1 _index))
    })
}))
```
