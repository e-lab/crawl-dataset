require 'nn'
require 'cunn'
require 'cudnn'
require 'paths'
require 'image'
require 'utils'
local opts = require 'opts'
opt = opts.parse()
print(opt)

function checkClassExist(class)
  for i in pairs(classes) do
    if classes[i] == class then
      return true
    end
  end
  return false
end

function getClass (o, c, i, truepath, falsepath, resizeFail)
   local iPath = paths.concat(o,c,i)
   local input
   local eye = 224

   --crop and resizing

 local function resize_image(iPath, dim, inner_crop, offset)
    local crop_mode = (inner_crop and ('^'..dim)) or tostring(dim)
    local outer_crop = not inner_crop


    -- load and rescale image from iPath
    local x = image.load(iPath)
    print('Law image size')
    print(x:size())
--    x = image.scale(x, crop_mode)

    -- consider 2-dim image
    x = ((x:dim() == 2) and x:view(1, x:size(1), x:size(2))) or x

    -- consider greyscale image
    x = ((x:size(1) == 1) and x:repeatTensor(3,1,1)) or x

    -- consider RGBA image
    x = ((x:size(1) > 3) and x[{{1,3},{},{}}]) or x

    local cs , y
    if x:size(2) > x:size(3) then
       cs = x:size(3)
    else
       cs = x:size(2)
    end
    x = image.crop(x,'c',cs,cs)
    y = image.scale(x,eye,eye)

--[[
    -- calculate coordinate for crop (left top of box)
    local lbox = math.floor(math.abs(x:size(3) - dim)/2 + 1)
    local tbox = math.floor(math.abs(x:size(2) - dim)/2 + 1)

    -- copy paste to y depending on crop_mode
    local y
    if inner_crop then
       y = x[{{},{tbox,tbox+dim-1},{lbox,lbox+dim-1}}]
    elseif outer_crop then
       y = torch.Tensor():typeAs(x):resize(3, dim, dim):fill(offset)
       y[{{},{tbox,tbox+x:size(2)-1},{lbox,lbox+x:size(3)-1}}]:copy(x)
    end
--]]
    return y
 end
   --check if it's resized successfully or not
   s =  pcall(function() input = resize_image(iPath, eye, true, 0) end)
   if not s then table.insert(resizeFail,iPath) end
   --Check input size
   print('Check input size')
   print(input:size())

--   input = torch.FloatTensor(img:size(1),eye,eye)
   for ch=1,3 do -- channels
      input[ch]:add(-mean[ch])
      input[ch]:div(std[ch])
   end
   input = input:resize(1,3,eye,eye)

   --Do prediction
   model:evaluate()
   model:cuda()
   output = model:forward(input:cuda())
   probs, indexes = output:topk(1, true, true)

   --Brian can you add below option? 
   --Get probability of c(folder name of input image)
   --And do probability > opt. th 

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
   if class == c and tonumber(prob) >= opt.th then
      toPath = paths.concat(truepath, i)
      file.copy(iPath, toPath)
      -- print('TRUE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
   else
      toPath = paths.concat(falsepath, i)
      file.copy(iPath, toPath)
      -- print('FALSE: file copied from\n' .. iPath .. '\nto\n' .. toPath)
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
resizeFail = {}


-- Main loop
filteredTrueDatasetPath = paths.concat(opt.src, 'filteredFalseDataSet')
filteredFalseDatasetPath = paths.concat(opt.src, 'filteredTrueDataSet')
checkPaths(filteredTrueDatasetPath)
checkPaths(filteredFalseDatasetPath)

--Iterates through all subdirectories of dataset folder
for c in paths.files(opt.src) do
   check = checkClassExist(c)
   if c ~= '..' and c ~= '.' and c~= 'filteredFalseDataSet' and c ~= 'filteredTrueDataSet' and check then
      --create folders for correct and incorrect class predictions, ex: sofaTRUE and sofaFALSE
      truepath = paths.concat(opt.src, 'filteredTrueDataSet', c )
      falsepath = paths.concat(opt.src, 'filteredFalseDataSet', c )
      --Check path exist if not creath dir
      flag = checkPaths(truepath)
      flag = checkPaths(falsepath)

      -- Check if work has been done with flag is true do work
      if flag then
         p = paths.concat(opt.src, c)
         for i in paths.files(p) do
            if i ~= '..' and i ~= '.' then
               getClass(opt.src, c, i, truepath, falsepath, resizeFail)
            end
         end
         collectgarbage()
      end
      print(resizeFail)
      resizeFail = {}
   end
end

--Create CSV file to save this table or txt
torch.save('resizeFailTable.t7',resizeFail)




