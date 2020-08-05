#!/usr/bin/env ruby -wKU

class Lexer
	attr_reader :tokens

	def initialize
		@KeyWords = ["@meta", "@brief", ]
		@tokens = []
	end

	def tokenize(code)
		i = 0

		while i < code.size
			chunk = code[i..-1]

			if identifier = chunk[/\A(@[a-z]\w*)/, 1]
				if @KeyWords.include?(identifier)
					@tokens << [identifier.upcase.to_sym]
				end

				i += identifier.size
			end

			i += 1
		end
	end
end

l = Lexer.new
l.tokenize("@meta ppharel")
puts("===TOKENS===")
puts(l.tokens)