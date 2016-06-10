prediction = {}

local function preprocess(dst, stat)
   require 'image'
   local cr_size
   local eye , mean, std = 224 , stat.mean, stat.std

   if dst:dim() == 3 then
      if dst:size(2) >= dst:size(3) then
         cr_size = dst:size(3)
      else
         cr_size = dst:size(2)
      end
   elseif dst:dim() == 4 then
      if dst:size(3) >= dst:size(4) then
         cr_size = dst:size(4)
      else
         cr_size = dst:size(3)
      end
   end

   input = image.crop(dst, 'c', cr_size, cr_size)
   input = image.scale(input,eye,eye)

   for ch=1,3 do -- channels
      input[ch]:add(-mean[ch])
      input[ch]:div(std[ch])
   end
   input:reshape(input,1,3,eye,eye)
   return input
end

local function init_(dst, model, stat)
   local input = nil
    prediction.forward =
    function (dst)
       input = preprocess(dst, stat)
       output = model:forward(input:cuda())
       return output
    end
end

function prediction:init(dst, model, stat)
   init_(dst, model, stat)
end

return prediction
