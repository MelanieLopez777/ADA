# color_palette.py

class ColorPalette:
    colors = {
        "Spring Green": {
            "hex": "#C6DA83",
            "rgb": (198, 218, 131),
            "cmyk": (9, 0, 40, 15)
        },
        "Azalea Pink": {
            "hex": "#F0849E",
            "rgb": (240, 132, 158),
            "cmyk": (0, 35, 25, 16)
        },
        "Baby Blue": {
            "hex": "#D6E6FD",
            "rgb": (214, 230, 253),
            "cmyk": (0, 45, 34, 6)
        },
        "Denim Blue": {
            "hex": "#4A4F87",
            "rgb": (74, 79, 135),
            "cmyk": (45, 41, 0, 47)
        },
        "Blush Pink": {
            "hex": "#D58A9F",  
            "rgb": (213, 138, 159),
            "cmyk": (0, 35, 25, 16)
        },
        "Ligth Grey": {
            "hex": "#E9EBF2",  
            "rgb": (233, 235, 242),
            "cmyk": (0.04, 0.03, 0.00 ,0.05)
        }
    }

    @classmethod
    def get_hex(cls, name):
        return cls.colors[name]["hex"]

    @classmethod
    def get_rgb(cls, name):
        return cls.colors[name]["rgb"]

    @classmethod
    def get_cmyk(cls, name):
        return cls.colors[name]["cmyk"]
    
    @classmethod
    def get_rgb_normalized(cls, name):
        r, g, b = cls.colors[name]["rgb"]
        return (r/255, g/255, b/255)
    
    @classmethod
    def get_color_list(cls, format="hex"):
        """Devuelve todos los colores en el formato especificado"""
        return [cls.colors[name][format] for name in cls.colors]