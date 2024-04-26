from os import walk, path, rename
import yaml

root_dir = f"{path.dirname(path.realpath(__file__))}/../device-types"
# root_dir = f"{path.dirname(path.realpath(__file__))}/../device-types/Cisco"

total = 0

for root, dirs, files in walk(root_dir):
  for file in files:
    if file.split(".")[1] == "yaml" or file.split(".")[1] == "yml":
      fileChanged = False
      if file.split(".")[0].count("_") > 0:
        newname = file.replace("_", "-")
        rename(f"{root}/{file}", f"{root}/{newname}")
      
print(f"Total Left: {total}")