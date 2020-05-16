import sys

from PIL import Image
import piexif


def get_camera(dict):
    manufacturer = str(dict["0th"][271], "utf-8")
    camera_type = str(dict["0th"][272], "utf-8")

    if manufacturer is None and camera_type is None:
        print("Camera manufacturer and type cannot be determined")
    else:
        print("Camera manufacturer:", manufacturer)
        print("Camera type:", camera_type)

    count = 0
    for tag in dict:
        if dict[tag] is not None:
            if len(dict[tag]) != 0:
                count += 1
    print("Count of EXIF IFDs:", count)


def get_exif(dict):
    data = dict.pop("Exif")
    print()
    if len(data) == 0:
        print("Exif IFD does not exist.")
    else:
        print("Exif IFD exists")
        print("Count of Exif IFD entries:", len(data))

        print()
        for tag in data:
            print(piexif.TAGS["Exif"][tag]["name"], data[tag])
    return data


def get_zeroth(dict):
    data = dict.pop("0th")
    print()
    if len(data) == 0:
        print("Primary IFD does not exist.")
    else:
        print("Primary IFD exists")
        print("Count of Primary IFD entries:", len(data))

        print()
        for tag in data:
            print(piexif.TAGS["0th"][tag]["name"], data[tag])
    return data


def get_first(dict):
    data = dict.pop("1st")
    print()
    if len(data) == 0:
        print("Additional IFD does not exist.")
    else:
        print("Additional IFD exists")
        print("Count of Additional IFD entries:", len(data))

        print()
        for tag in data:
            print(piexif.TAGS["1st"][tag]["name"], data[tag])
    return data


def get_gps(dict):
    data = dict.pop("GPS")
    print()
    if len(data) == 0:
        print("GPS IFD does not exist.")
    else:
        print("GPS IFD exists")
        print("Count of GPS IFD entries:", len(data))

        print()
        for tag in data:
            print(piexif.TAGS["GPS"][tag]["name"], data[tag])
    return data


def get_interop(dict):
    data = dict.pop("Interop")
    print()
    if len(data) == 0:
        print("Interop IFD does not exist.")
    else:
        print("Interop IFD exists")
        print("Count of Interop IFD entries:", len(data))

        print()
        for tag in data:
            print(piexif.TAGS["Interop"][tag]["name"], data[tag])
    return data


def get_thumbnail(dict):
    data = dict.pop("thumbnail")
    print()
    if data is None:
        print("Thumbnail does not exist")
    else:
        print("Thumbnail exists")
    return data


path = sys.argv[1]

exif_dict = piexif.load(path)
im = Image.open(path)

get_camera(exif_dict)
exif = get_exif(exif_dict)
zeroth = get_zeroth(exif_dict)
first = get_first(exif_dict)
gps = get_gps(exif_dict)
interop = get_interop(exif_dict)
thumbnail = get_thumbnail(exif_dict)
print("quantization tables:")
print(im.quantization[0])
print(im.quantization[1])
