class Dataunits:
    class DataType(Enum):
        unknown = 0 #we will try to infer type
        byte = 1 #base measurement in bytes, such as MB, gb, etc.
        bits8 = 8 #standard data storage/transfer using 8 bits such as mbps or mbits. If inferred, 8 bits will be assumed
        bits10 = 10 #data transfer using 10 bits using 8 bits such as mbps or mbits
        
    class Units(Enum):
        Base = 0
        Kilo = 1
        Mega = 2
        Giga = 3
        Tera = 4
        Peta = 5
    
    class UnitsBase(Enum):
        SI = 1000
        Binary = 1024
        
    def __init__(self, strNum, numType = DataType.unknown, debug=False):
        self.debug = debug
        self.strOrig = strNum
        self.numType = numType
        self.unitsOrigStr = self._extractstrunits() #the units extracted from string with number and units
        self.numOrig = self._extractnumber() #the number extracted from string with number and units
        self.units = self._getunits() #Convert the unit string to enum
        self.numType = self._inferdatatype() #this will leave the value alone unless it an unknown type, where it will try to confirm bytes or bits8
        self.unitsbase = self._getunitsbase() #this determines if value is in bytes, if so, use Binary, otherwise use SI
        self.numRawBytes = self._calcnumraw() #this is the value in bytes of the number, taking into account the UnitsBase
        self.numInUnits = self.numOrig #start with the orig num cause units, type, and base are correct for this number
        
        if debug: 
            print("strOrig = " + self.strOrig + "; numType = " + str(self.numType) + "; unitsOrigStr = " + self.unitsOrigStr + 
                "; numOrig = " + str(self.numOrig) + "; units = " + str(self.units) + "; unitsbase = " + str(self.unitsbase) + "; numRawBytes = " + str(self.numRawBytes) + 
                "; numInUnits = " + str(self.numInUnits) )

    def convertunits(self, newUnits, newType = DataType.byte):
        num = self.numRawBytes
        if self.DataType.byte == newType:
            return int(self.numRawBytes / (self.unitsbase.value**newUnits.value) )
        elif self.DataType.bits8 == newType:
            return int((self.numRawBytes * 8 )/ (self.unitsbase.value**newUnits.value) ) 
        elif self.DataType.bits10 == newType:
            return int((self.numRawBytes * 10)/ (self.unitsbase.value**newUnits.value) ) 
            
    def _extractnumber(self, strNum = ""):
        p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        nums = []
        if strNum != "":
            self.strOrig = strNum
        if re.search(p, self.strOrig) is not None:
            for catch in re.finditer(p, self.strOrig):
                nums.append(int(catch[0])) # catch is a match object
        if self.debug: print(nums)
        if len(nums) > 0:
            return nums[0]
        return 0

    def _extractstrunits(self, strNum = ""):
        p = '[a-zA-Z]+'
        strs = []
        if strNum != "":
            self.strOrig = strNum
        if re.search(p, self.strOrig) is not None:
            for catch in re.finditer(p, self.strOrig):
                strs.append(catch[0]) # catch is a match object
        if self.debug: print(strs)
        if len(strs) > 0:
            return strs[0]
        return ""

    def _calcnumraw(self):
        nRaw = self.numOrig
        if self.numType == self.DataType.byte:
            nRaw = (self.unitsbase.value**self.units.value) * self.numOrig
        elif self.numType == self.DataType.bits8: #if in bits, store in bytes, easier to work with
            nRaw = int(((self.unitsbase.value**self.units.value) * self.numOrig) / self.DataType.bits8.value)
        elif self.numType == self.DataType.bits10:
            nRaw = int(((self.unitsbase.value**self.units.value) * self.numOrig) / self.DataType.bits10.value)
        return nRaw

    def _getunits(self):
        e = 0 #exponent
        c = ""
        if len(self.unitsOrigStr) >= 1:
            c = self.unitsOrigStr[0].lower()
        if c == "p": e = self.Units.Peta
        elif c == "t": e = self.Units.Tera
        elif c == "g": e = self.Units.Giga
        elif c == "m": e = self.Units.Mega
        elif c == "k": e = self.Units.Kilo
        else: e = self.Units.Base
        if self.debug: print("GetMultiplier\nc = " + c + "  e = " + str(e))

        return e
        
    def _inferdatatype(self):
        t = self.numType
        if self.numType == self.DataType.unknown and len(self.unitsOrigStr) > 0: #ignore this unless unknown
            t = self.DataType.unknown
            if self.debug: print("Infer Datatype\nunitsOrigStr = " + self.unitsOrigStr[:2] + " len = " + str(len(self.unitsOrigStr)))
            #try to infer type
            if 'b' in self.unitsOrigStr[:2]: t = self.DataType.bits8 #not-well-used convention where small b means bits.
            elif 'B' in self.unitsOrigStr[:2]: t = self.DataType.byte
            
            if "bit" in self.unitsOrigStr.lower(): t = self.DataType.bits8
            elif "byte" in self.unitsOrigStr.lower(): t = self.DataType.byte
            
            if t == self.DataType.unknown:
                t = self.DataType.byte #if cannot be determined, assume bytes
                if self.debug: print("Could not determine type, defaulting to bytes")
        return t
        
    def _getunitsbase(self): 
        b = self.UnitsBase.SI
        if self.numType == self.DataType.byte: b = self.UnitsBase.Binary
        return b
