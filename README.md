# ArkDoc

It's **Lite** documentation gen for arkscript (.ark) based on Mkdocs, and write in ruby. You probably think : you created a programming language and you don't use it, but for to answer you : _yes, we will probably use ArkScript in a next one update_.


## Dependencies

+ Python 2.7 or higher

+ Ruby 2.5 or higher


## Usage

```bash
# Clone repository
~$ git clone https://github.com/ArkScript-lang/ArkDoc.git
# It's in this folder the doc site will build
~/ArkDoc$ mkdir docs
# Put your arkscripts in this folder 
~/ArkDoc$ mkdir ark
# Install Mkdocs
~$ pip install mkdocs 
# Build site in docs/[SITE_NAME]/site
~/ArkDoc$ ruby start.rb gen [SITE_NAME]
```


## Syntax

`\` : For function brief begin

`@` : For function parameter 

\` code example \` : code example

`!` : Page title

`/` : Escape character (place this char before you special char to avoid md conversion )


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