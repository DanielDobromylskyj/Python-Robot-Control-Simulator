
class Material:
    static: float
    dynamic: float
    density: float
    name: str

    def __init__(self, name: str, static: float, dynamic: float, density):
        """ Stores properties of a given material including its friction coefficients and its density in kg/m3"""
        self.name = name
        self.static = static
        self.dynamic = dynamic
        self.density = density


steel =     Material("Steel", 0.60, 0.40, 7850)
aluminium = Material("Aluminium", 0.55, 0.35, 2700)
wood =      Material("Wood", 0.50, 0.30, 700)
glass =     Material("Glass", 0.40, 0.25, 2500)
rubber =    Material("Rubber", 1.00, 0.80, 1100)
concrete =  Material("Concrete", 0.80, 0.60, 2400)
ice =       Material("Ice", 0.10, 0.03, 917)
plastic =   Material("Plastic", 0.40, 0.25, 1200)
pla =       Material("PLA", 0.40, 0.30, 1240)
nylon =     Material("Nylon", 0.30, 0.20, 1150)
ptfe =      Material("PTFE", 0.10, 0.05, 2200)
asphalt =   Material("Asphalt", 0.80, 0.60, 2400)
sand =      Material("Sand", 0.70, 0.50, 1600)
