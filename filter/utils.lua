function checkPaths(path, flag)
--delete filtereddataset folder and creates a new one
--paths.rmall(filteredDatasetPath, 'yes')
--paths.mkdir(filteredDatasetPath)
   if not paths.dirp(path) then
      paths.mkdir(path)
      --Flag for do classify
      flag = true
   else
      print(path .. ' already exist')
      flag = false
   end
   --print('Flag : ' .. tostring(flag))
   return flag
end
