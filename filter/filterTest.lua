require 'nn'
require 'cudnn'
require 'paths'
require 'image'

opts = assert(require'opts')
lapp = require 'pl.lapp'
opt = lapp[[
 -r, --root        (default 'res34AugLast')
 -m, --model       (default 'model_7.t7')
 -c, --classes     (default 'classes.t7')
 -s, --stat        (default 'stat.t7')
 -d, --dst         (default 'dst')     Destination dir
 -s, --src         (default 'sofa')     Soruce dir
 --manualSeed      (default 1)
 --GPU             (default 1)
]]

print(opt)
cutorch.setDevice(opt.GPU) -- by default, use GPU 1
torch.manualSeed(opt.manualSeed)

root    = opt.root
mPath   = paths.concat(root, opt.model)
cPath = paths.concat(root, opt.classes)
sPath    = paths.concat(root, opt.stat)

model   = torch.load(mPath)
classes = torch.load(cPath)
stat    = torch.load(sPath)
std     = stat.std
mean    = stat.mean

print(std)
print(mean)
--Create Functions below
--Create New Folders if not exist e.g. TrueSofa FalseSofa

--Do all the images in the folder repeatedly
iPath = paths.concat(opt.src,'sofa_99.jpeg')
local input, img
local eye = 224
--load Image
input = image.load(iPath)
--Make image appliable to the model (preprocessing)
local cr_size
if input:dim() == 3 then
   if input:size(2) >= input:size(3) then
      cr_size = input:size(3)
   else
      cr_size = input:size(2)
   end
elseif input:dim() == 4 then
   if input:size(3) >= input:size(4) then
      cr_size = input:size(4)
   else
      cr_size = input:size(3)
   end
end
input = image.crop(input, 'c', cr_size, cr_size)
input = image.scale(input,eye,eye)
for ch=1,3 do -- channels
   input[ch]:add(-mean[ch])
   input[ch]:div(std[ch])
end
input:reshape(input,1,3,eye,eye)

--Check input size
print(input:size())

--Do prediction
model:evaluate()
output = model:forward(input:cuda())
probs, indexes = output:topk(1, true, true)

--sofa  == 17
--Check with classes
for i in pairs(classes) do
   if i == indexes:squeeze() then
   print(classes[i])
   end
end

--Create Functions below
--If Folder name and prediction is match then move to TrueSofa else FalseSofa folder




