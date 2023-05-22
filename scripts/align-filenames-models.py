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
        
      data = []
      with open(path.join(root, file), 'r') as stream:
        try:
          data = stream.readlines()
          
          model = ""
          partNumber = ""
          
          for idx, line in enumerate(data):
            if "model: " in line:
              model = line.split(": ")[1].strip().replace(" ", "-")
            if "part_number: " in line:
              partNumber = line.split(": ")[1].strip()
          
          fileName = file.split('.')[0].casefold()
          regModel = model.replace("sfp+", "sfpp").replace("poe+", "poep").replace("!", "").replace("/", "-").replace("SFP+", "SFPP").replace("POE+", "POEP").replace("!", "").replace("/", "-").replace("PoE+", "PoEP")
          modModel = regModel.casefold().replace("'", "").replace("+", "-plus").replace("*", "-")
          if modModel not in fileName and partNumber.casefold() not in fileName:
            print("------------")
            print(regModel.replace("sfp+", "sfpp").replace("poe+", "poep").replace("!", "").replace("/", "-").replace("SFP+", "SFPP").replace("POE+", "POEP").replace("!", "").replace("/", "-").replace("PoE+", "PoEP").replace("+", "-plus").replace("*", "-"))
            print(partNumber.casefold())
            print(file.casefold())
            print("------------")
            total = total + 1
          
        except yaml.YAMLError as exc:
          print(exc)
        stream.close()
      
print(f"Total Left: {total}")