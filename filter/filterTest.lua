require 'nn'
require 'cudnn'
require 'paths'
require 'image'
require 'utils'
local opts = require 'opts'
opt = opts.parse()
print(opt)
function getClass (o, c, i, truepath, falsepath)
   iPath = paths.concat(o,c,i)
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

   index = indexes:squeeze()
   prob = math.exp(probs:squeeze())
   class = classes[index]

   print('Class: ')
   print(class)
   print('Probability: ')
   print(prob)
   print('File path: ')
   print(iPath)

   --moves images to corresponding folders based on filter response
   if class == c and tonumber(prob) >= 0.5 then
      toPath = paths.concat(truepath, i)
      file.copy(iPath, toPath)
      print('TRUE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
   else
      toPath = paths.concat(falsepath, i)
      file.copy(iPath, toPath)
      print('FALSE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
   end

   -- for i in pairs(classes) do
   --    if i == indexes:squeeze() then
   --       print('Classes:')
   --       print(classes[i])
   --       probs = probs:squeeze()
   --       print('Probability: ')
   --       print(math.exp(probs))
   --       print('File path: ')
   --       print(iPath)
   --    end
   -- end
end

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
flag = false


-- Main loop
filteredDatasetPath = paths.concat(opt.src, 'filteredDataSet')
checkPaths(filteredDatasetPath)

--Iterates through all subdirectories of dataset folder
for c in paths.files(opt.src) do
   if c ~= '..' and c ~= '.' and c~= 'filteredDataSet' then
      --create folders for correct and incorrect class predictions, ex: sofaTRUE and sofaFALSE
      truepath = paths.concat(opt.src, 'filteredDataSet', c .. "TRUE")
      falsepath = paths.concat(opt.src, 'filteredDataSet', c .. "FALSE")
      --Check path exist if not creath dir
      flag = checkPaths(truepath)
      flag = checkPaths(falsepath)
      -- Check if work has been done with flag is true do work
      if flag then
         p = paths.concat(opt.src, c)
         for i in paths.files(p) do
            if i ~= '..' and i ~= '.' then
               getClass(opt.src, c, i, truepath, falsepath)
            end
         end
      end
   end
end





