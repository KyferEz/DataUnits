# DataUnits
This is designed to take a alphanumeric string indicating storage size and determine the actual value. For example, if you have 410MB, it will be able to determine that this is 410*1024*1024 bytes and provide that number as well as it's constituents.

Example usage:
    num = Dataunits("410M", numType=Dataunits.DataType.unknown, debug=True)
    print(num.convertunits(num.Units.Kilo, num.DataType.bits8))
    print(str(num.units))
