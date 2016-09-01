-- By Sangpil Kim
-- July 2016
-- Test Filter for edataset
require 'pl'
lapp = require 'pl.lapp'

local opts = {}

--This is example for opt lua code will add in a filter module
function opts.parse()
   local opt = lapp[[
    -r, --root        (default '') Root folder path of model
    -m, --model       (default '') model name Ex model_7.t7
    -c, --classes     (default 'classes.t7') classes.t7
    -s, --stat        (default 'stat.t7') stat.t7
    -d, --dst         (default 'dst')     Destination dir
    --src             (default '')     Source dir
    --manualSeed      (default 1)
    --GPU             (default 1)
    --th              (default 0.3)      Threshold
   ]]
   return opt
end

return opts

