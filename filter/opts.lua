-- By Sangpil Kim
-- July 2016
-- Test Filter for edataset
require 'pl'

local opts = {}

--This is example for opt lua code will add in a filter module
function opts.parse(arg)
   local opt = lapp [[
   Command line options:
   -m, --model       (default '/media/HDD1/flickr/checkpoints/res34AugFine/model_17.t7')   Model path
   -c, --classes     (default '/media/HDD1/flickr/checkpoints/res34AugFine/classes.t7') Classes categories
   -d, --dst         (default 'dst')     Destination dir
   -s, --src         (default 'src')     Soruce dir
   ]]
   return opt
end

return opts

