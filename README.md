# ArkDoc

It's a **Lite** documentation generator for arkscript (.ark) based on Mkdocs, and written in ruby. You probably think: you created a programming language and you don't use it, but to answer you : _yes, we will probably use ArkScript in a next update_.


## Dependencies

* Python >= 2.7 (Python 3.7 tested and working)
* Ruby >= 2.5

## Usage

```bash
# Clone repository
~$ git clone https://github.com/ArkScript-lang/ArkDoc.git
# The documentation will be generated in this folder
~/ArkDoc$ mkdir docs
# Put your arkscripts in this folder
~/ArkDoc$ mkdir ark
# Install Mkdocs
~$ pip install mkdocs 
# Build site in docs/[SITE_NAME]/site
~/ArkDoc$ ruby start.rb gen [SITE_NAME]
```

## Syntax

`\`: For function brief begin

`@`: For function parameter 

\` code example \`: code example

`!`: Page title

`/`: Escape character (place this char before any special char to avoid md conversion)

## Example
```clojure
{
	#(([Home]index)
	#!Numeric
	#\fibo Calcul fibonacci sequence with n
	#@n a number
	#`
	#	{
	#		(let fibo (fun (n)
	#			(if (< n 2)
	#				n
	#			(+ (fibo (- n 1)) (fibo (- n 2))))))
	#
	#		(print (fibo 28))  # display 317811
	#	}
	#`
	#)
	(let fibo (fun (n)
		(if (< n 2)
			n
		(+ (fibo (- n 1)) (fibo (- n 2))))))
}
```
![basic mode](./images/example.png)