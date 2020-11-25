# Syntax

The new syntax is inspired by doxygen syntax.

The content of documentation must be in a block and each line must begin by comment char (for arkscript hash **#**), using this syntax.
Exanple :
```
###
#...documentation content
##
```
## Main keywords

`@meta` : page informations (title, desciprtion of page or section), create new page at every call, then only one call for every files to avoid undefined behavior of parser.

`@brief` : speed function presentation

`@details` : details about function (object modification)

`@param` : explanation or details about each  parameter of function

`@author` : information about the author of the function

### Code example

Same as documentation content the example about function usage is a block, and you should use this syntax, for make a code example in arkdoc.
Example :

```
###
#...documentation content
# =begin
# ...example
# =end
##
```

### Full template

This template is a clean way to format your documentation in source file, for a good transformation in page

```clojure
###
# @brief (description of function)
# @param (details about each parameter of function)
# @details (details about impact of function on a object or paramater)
# =begin
# (example)
# =end
# @author (where we can find the author of function code)
##
```