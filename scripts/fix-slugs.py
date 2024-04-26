from os import walk, path
import yaml

root_dir = f"{path.dirname(path.realpath(__file__))}/../device-types"
# root_dir = f"{path.dirname(path.realpath(__file__))}/../device-types/Cisco"

total = 0

for root, dirs, files in walk(root_dir):
  for file in files:
    if file.split(".")[1] == "yaml" or file.split(".")[1] == "yml":
      fileChanged = False
      data = []
      with open(path.join(root, file), 'r') as stream:
        try:
          data = stream.readlines()
          # data = yaml.safe_load(stream)

          slugManufacturer = ""
          slugManufacturerIDX = 0
          slug = ""
          slugIDX = 0
          model = ""
          modelIDX = 0
          partNumber = ""
          partNumberIDX = 0

          for idx, line in enumerate(data):
            if "manufacturer: " in line:
              # slugManufacturer = data['manufacturer'].casefold().replace(" ", "-")
              slugManufacturer = line.split(": ")[1].casefold().replace(" ", "-").strip()
              slugManufacturerIDX = idx
            if "slug: " in line:
              slug = line.split(": ")[1].strip()
              slugIDX = idx
            if "model: " in line:
              model = line.split(": ")[1].strip()
              modelIDX = idx
            if "part_number: " in line:
              partNumber = line.split(": ")[1].strip()
              partNumberIDX = idx

          transformedModel = model.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
          transformedPartNumber = partNumber.casefold().replace(" ", "-").replace("-+", "-plus").replace("+", "-plus-").replace("_", "-").replace("&", "-and-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")
          transformedManufacturer = slugManufacturer.casefold().replace(" ", "-").replace("sfp+", "sfpp").replace("poe+", "poep").replace("-+", "-plus-").replace("+", "-plus").replace("_", "-").replace("!", "").replace("/", "-").replace(",", "").replace("'", "").replace("*", "-")

          if "&" in transformedManufacturer:
            transformedManufacturer = transformedManufacturer.replace("&", "-and-")
            if "--and--" in transformedManufacturer:
              transformedManufacturer = transformedManufacturer.replace("--and--", "-and-")

          newSlug = f"{transformedManufacturer}-{transformedModel}"
          newPartSlug = f"{slugManufacturer}-{transformedPartNumber}"
          newComboSlug = f"{slugManufacturer}-{transformedModel}-{transformedPartNumber}"
          slugManufacturerDash = f"{slugManufacturer}-"
          if slugManufacturer != "apple":
            if newSlug.count(slugManufacturerDash) > 1:
              newSlug = newSlug.replace(f"{slugManufacturer}-", "", 1)
            if newPartSlug.count(slugManufacturerDash) > 1:
              newPartSlug = newPartSlug.replace(f"{slugManufacturer}-", "", 1)
            if newComboSlug.count(slugManufacturerDash) > 1:
              newComboSlug = newComboSlug.replace(f"{slugManufacturer}-", "", 1)

            if newSlug[-1] == "-":
                newSlug = newSlug[:-1]
            if newSlug != slug and newPartSlug != slug and newComboSlug != slug:
              print(f"{newSlug} != {slug}")
              data[slugIDX] = f"slug: {newSlug}\n"
              total = total + 1
              fileChanged = True

        except yaml.YAMLError as exc:
          print(exc)
        stream.close()

      if fileChanged:
        with open(path.join(root, file), 'w') as file:
          file.writelines(data)
          file.close()

print(f"Total Left: {total}")