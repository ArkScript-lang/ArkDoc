#!/usr/bin/env ruby -wKU

class String
	
	def to_a
		ary = []

		self.each_line { |line|
			ary.push(line)
		}

		return ary
	end
end