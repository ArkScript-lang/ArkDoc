#!/usr/bin/env ruby -wKU

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
end