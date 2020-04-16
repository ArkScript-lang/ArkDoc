#!/usr/bin/env ruby -wKU
require "syntax.rb"
Alpha = /[[:alpha:]]/

class String
	
	def to_a
		ary = []

		self.each_line { |line|
			ary.push(line)
		}

		return ary
	end

	def end
		return (self.size - 1)
	end

	def add_nw
		buf = ""

		self.each_char { |c|
			if c == NewLine
				buf << NewLine
			end

			buf << c
		}

		self.replace(buf)
	end
end