-- Author: Aysegul Dundar
-- Date: December, 2014
require 'image'
require 'trepl'
require 'paths'
require 'pl'

opt = lapp[[
   -f,--flip              (default true)        horizontal flip
   -t,--transImgInt        (default 20)          stepping of translation, number of images to create (ta/t)^2
   --ta                    (default 40)          max translation length
   -r, --rotationImg       (default 2)           number of images to create by rotation
   --ra                    (default 0.1)         max angle of rotation
   -p,--pathToRoot       (default 'images')    path to the folder of images
]]

if not paths.dir(opt.pathToRoot) then
  error(string.format("the folder %s not exist", opt.pathToRoot))
end



function hflip_img(path_img, tmp_img, aug_path, img)
  local tmp_path = path_img .. "/" .. tmp_img
  local img_flip = image.hflip(img)
  -- assumes .png ending for now
  tmp_img = string.sub(tmp_img, 1, -5)
  local img_path = aug_path .. "/" .. tmp_img .. "hflip.png"
  image.save(img_path, img_flip)

end
function vflip_img(path_img, tmp_img, aug_path, img)
  local tmp_path = path_img .. "/" .. tmp_img
  local img_flip = image.vflip(img)
  -- assumes .png ending for now
  tmp_img = string.sub(tmp_img, 1, -5)
  local img_path = aug_path .. "/" .. tmp_img .. "vflip.png"
  image.save(img_path, img_flip)

end

function rotate_img(path_img, tmp_img, aug_path, degree, img)

  local tmp_path = path_img .. "/" .. tmp_img
  local img_rotate = image.rotate(img, degree)

  -- assumes .png ending for now
  tmp_img = string.sub(tmp_img, 1, -5)
  local img_path = aug_path .. "/" .. tmp_img ..  "rotate" .. degree .. ".png"
  image.save(img_path, img_rotate)
  if opt.flip == true then
     hflip_img(aug_path, tmp_img .. "rotate" .. degree .. ".png", aug_path,img_rotate)
  end

end


function crop5_img(path_img, tmp_img, aug_path, jitter, img)

  local tmp_path = path_img .. "/" .. tmp_img

  local w = img:size(2) - jitter
  local h = img:size(3) - jitter

  -- assumes .png ending for now
  tmp_img = string.sub(tmp_img, 1, -5)

  local number_img = jitter/opt.transImgInt

  for i=1, number_img do
    for j=1, number_img do
       local sample = img[{{}, {1+ (j-1) * opt.transImgInt, (j-1) * opt.transImgInt + w},
                               {1+ (i-1) * opt.transImgInt, (i-1) * opt.transImgInt + h}}]
       local img_path = aug_path .. "/" .. tmp_img .. "crop" .. (j+(i-1)*number_img) .. ".png"
       image.save(img_path, sample)


       if opt.flip == true then
         hflip_img(aug_path, tmp_img .. "crop" .. (j+(i-1)*number_img) .. ".png", aug_path,sample)
       end

     end
   end

end
function run_on_folder(root_path,folder_name)
   src_path = paths.concat(root_path,folder_name)..'/'
   local image_names = paths.dir(src_path, 'r')
   local aug_path = paths.concat("./augmentations/",folder_name)
   if not paths.dirp(aug_path) then
      os.execute("mkdir -p " ..aug_path)
   end
   for i=1, #image_names do

     local tmp_img = image_names[i]
     if (string.sub(tmp_img, 1, 1) ~= '.' and tmp_img ~= 'augmentations') then
         src_img_path = src_path .. tmp_img
         local img = image.load(src_img_path)
         if img:size(1) > 3 then img = img:narrow(1,1,3) end

         if opt.ta > 0 then
            crop5_img(src_path, tmp_img, aug_path, opt.ta, img)
         end

         if opt.flip == true then
            hflip_img(src_path, tmp_img, aug_path, img)
         end

         if opt.ra > 0 then
            local angle = opt.ra/opt.rotationImg
            for i=1, opt.rotationImg do
                rotate_img(src_path, tmp_img, aug_path, angle*i, img)
             end
         end
     end
   end
end
function mv_images(root_path,folder_name)
   target_folder = paths.concat('./augmentations/',folder_name)
   folder_path = paths.concat(root_path,folder_name)
   if not paths.dirp(target_folder) then
      os.execute("mkdir -p " ..target_folder)
   end
   os.execute('cp '..folder_path..'/*.png '..target_folder)
end
src_root_path = opt.pathToRoot
for folder_name in paths.iterdirs(src_root_path) do
   src_folder_path = paths.concat(src_root_path,folder_name)
   mv_images(src_root_path,folder_name)
   run_on_folder(src_root_path,folder_name)
end
