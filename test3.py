color = '#000000'

def rgb_to_hex(rgb:tuple) -> str:
    return '#%02x%02x%02x' % rgb

def hex_to_rgb(hex:str) -> tuple:
    value = hex.lstrip('#')

    rgbList = [int(value[i:i+2], 16) for i in range(0, len(value), 2)]

    return tuple(rgbList)

def change_color(hexColor:str, incrTuple:tuple=(0, 0, 0)) -> str:
    rgbColor = hex_to_rgb(hexColor)
    
    rgbColorNew = tuple([(rgbColor[index]+incrTuple[index])%256 for index in range(len(rgbColor))])

    return rgb_to_hex(rgbColorNew)


rgb_color = rgb_to_hex((255, 255, 255))

hex_color = hex_to_rgb(color)

newHexColor = change_color(color, (124, 51, 257))

print(rgb_color)

print(hex_color)

print(newHexColor)
