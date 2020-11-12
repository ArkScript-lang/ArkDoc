#!/usr/bin/env ruby -wKU

class String

    def refine
        return self.lstrip.delete_prefix("#").lstrip
    end

end