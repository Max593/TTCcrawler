class UrlBuilderException(Exception):
    pass



class UrlBuilder:
    #TODO make a build for item class 
    __itemCategory1IDDictionary = {
        "weapon"            :"0",
        "apparel"           :"1",
        "armor"             :"1",
        "soul gem & glyphs" :"2",
        "crafting"          :"3",
        "food & potions"    :"4",
        "other"             :"5",
        "furnishing"        :"6"
    }

    __itemCategory2IDDictionary = {
        "one handed"            : "0",
        "two handed"            : "1",
        "light"                 : "2",
        "medium"                : "3",
        "heavy"                 : "4",
        "shield"                : "5",
        "accesory"              : "6",
        "soul gem"              : "7",
        "armor glyph"           : "8",
        "weapon glyph"          : "9",
        "jewelry"               : "10",
        "alchemy"               : "11",
        "blacksmithing"         : "12",
        "clothing"              : "13",
        "enchanting"            : "14",
        "provisioning"          : "15",
        "woodworking"           : "16",
        "motif"                 : "17",
        "style material"        : "18",
        "armor trait"           : "19",
        "weapon trait"          : "20",
        "style raw material"    : "30",
        "master writ"           : "39",
        "jewelry crafting"      : "41",
        "jevelry trait"         : "42",
        "raw trait"             : "43",
        "food"                  : "21",
		"drink"                 : "22",
		"potion"                : "23",
		"poison"                : "32",
        "bait"                  : "24",
		"tool"                  : "25",
        "siege"                 : "26",
        "trophy"                : "27",
        "container"             : "28",
        "fish"                  : "29",
        "misc"                  : "31",
        "crafting station"      : "33",
		"light"                 : "34",
		"ornamental"            : "35",
		"seating"               : "36",
    	"target dummy"          : "37",
		"recipe"                : "38",
		"material"	            : "40"
    }

    __itemCategory3IDDictionary = {
        "axe"                       :"0",
		"mace"                      :"1",
		"sword"                     :"2",
		"dagger"                    :"3",
        "battleAxe"                 :"4",
		"greatSword"                :"5",
		"maul"                      :"6",
		"bow"                       :"7",
		"healing staff"             :"8",
		"inferno staff"             :"9",
		"ice staff"                 :"10",
		"lightning staff"           :"11",
        "l chest"                   :"12",
		"l feet"                    :"13",
		"l hand"                    :"14",
		"l head"                    :"15",
		"l legs"                    :"16",
		"l shoulders"               :"17",
		"l waist"                   :"18",
        "m chest"                   :"19",
		"m feet"                    :"20",
		"m hand"                    :"21",
		"m head"                    :"22",
		"m legs"                    :"23",
		"m shoulders"               :"24",
		"m waist"                   :"25",
        "h chest"                   :"26",
		"h feet"                    :"27",
		"h hand"                    :"28",
		"h head"                    :"29",
		"h legs"                    :"30",
		"h shoulders"               :"31",
		"h waist"                   :"32",
        "appearance"                :"33",
		"necklace"                  :"34",
		"ring"                      :"35",
        "potion base"               :"36",
		"reagent"                   :"37",
        "blacksmith raw material"   :"38", 
		"blacksmith material"       :"39",
		"blacksmith temper"         :"40",
        "clothing raw material"     :"41",
		"clothing material"         :"42",
		"clothing temper"           :"43",
        "aspect runestone"          :"44",
		"essence runestone"         :"45",
		"potency runestone"         :"46",
        "ingredient"                :"47",
		"recipe"                    :"48",
        "woodworking raw material"  :"49",
		"woodworking material"      :"50",
		"woodworking resin"         :"51",
        "jewelry raw material"      :"53",
		"jewelry material"          :"54",
		"jewelry plating"           :"55"
    }

    __itemTraitIdDictionary = {
	    "powered"           :"0",
	    "charged"           :"1",
	    "precise"           :"2",
	    "infused"           :"3",
	    "defending"         :"4",
	    "training"          :"5",
    	"sharpened"         :"6",
    	"decisive"          :"7",
    	"sturdy"            :"8",
    	"impenetrable"      :"9",
    	"reinforced"        :"10",
    	"well fitted"       :"11",
    	"invigorating"      :"12",
    	"divines"           :"13",
    	"nirnhoned"         :"14",
	    "intricate"         :"15",
	    "ornate"            :"16",
    	"arcane"            :"17",
    	"healthy"           :"18",
    	"robust"            :"19",
    	"special"           :"20",
    	"bloodthirsty"      :"21",
	    "harmony"           :"22",
    	"protective"        :"23",
    	"swift"             :"24",
    	"triune"            :"25"    
    }

    __itemQualityDictionary = {

        "normal"    : "0",
	    "fine"      : "1",
	    "superior"  : "2",
	    "epic"      : "3",
	    "legendary" : "4"
    }

    #convers itemNamePattern to conform to ttc url
    def __convertItemNamePattern(self,itemNamePattern):
        #ttc uses + in place of ' '
        itemNamePattern = itemNamePattern.replace(" ","+")

        #we have to change ' into %27
        itemNamePattern = itemNamePattern.replace("'","%27")
        return itemNamePattern

    #converts itemCategory1id from string name to id
    def __convertItemCategory1ID(self,itemCategory1id:str):
        if itemCategory1id == "":
            return ""
        if itemCategory1id not in self.__itemCategory1IDDictionary:
            raise UrlBuilderException("Given itemCategory1id not in dictionary")
        return self.__itemCategory1IDDictionary[itemCategory1id]

    #converts itemCategory2id from string name to id
    def __convertItemCategory2ID(self,itemCategory2id:str):
        if itemCategory2id == "":
            return ""
        if itemCategory2id not in self.__itemCategory2IDDictionary:
            raise UrlBuilderException("Given itemCategory2id not in dictionary")
        return self.__itemCategory2IDDictionary[itemCategory2id]

    #converts itemCategory3id from string name to id
    def __convertItemCategory3ID(self,itemCategory3id:str):
        if itemCategory3id == "":
            return ""
        if itemCategory3id not in self.__itemCategory3IDDictionary:
            raise UrlBuilderException("Given itemCategory3id not in dictionary")
        return self.__itemCategory3IDDictionary[itemCategory3id]

    #converts itemTraitId from string name to id
    def __convertItemTraitId(self,itemTraitId:str):
        if itemTraitId == "":
            return ""
        if itemTraitId not in self.__itemTraitIdDictionary:
            raise UrlBuilderException("Given itemTraitId not in dictionary")
        return self.__itemTraitIdDictionary[itemTraitId]

    #converts itemQualityId from string name to id
    def __convertItemQualityId(self,itemQualityId:str):
        if itemQualityId == "":
            return ""
        if itemQualityId not in self.__itemQualityDictionary:
            raise UrlBuilderException("Given itemQualityId not in dictionary")
        return self.__itemQualityDictionary[itemQualityId]

    

    #region can be either eu or na
    #platform can be: pc,xb,ps
    #itemNamePattern is a search string
    
    def build(self, region:str , platform:str , itemNamePattern:str , itemCategory1id:str , itemCategory2id:str , itemCategory3id:str , itemTraitId:str , itemQualityId:str,isChampionPoint:bool,levelMin:str,levelMax:str,masterWritVoucherMin:str,masterWritVoucherMax:str,amountMin:str,amountMax:str,priceMin:str,priceMax:str,page:str):
        
        urlString = "https://" + region + ".tamrieltradecentre.com/" + platform + "/Trade/SearchResult?ItemID=&TradeType=Sell&ItemNamePattern="

        #we add itemNamePattern
        urlString += self.__convertItemNamePattern(itemNamePattern)

        #we add itemCategory1ID
        urlString += "&ItemCategory1ID="
        urlString += self.__convertItemCategory1ID(itemCategory1id)

        #we add itemCategory2ID
        urlString += "&ItemCategory2ID="
        urlString += self.__convertItemCategory2ID(itemCategory2id)

        #we add itemCategory3ID
        urlString += "&ItemCategory3ID="
        urlString += self.__convertItemCategory3ID(itemCategory3id)

        #we add itemTraitID
        urlString += "&ItemTraitID="
        urlString += self.__convertItemTraitId(itemTraitId)

        #we add ItemQualityID
        urlString += "&ItemQualityID="
        urlString += self.__convertItemQualityId(itemQualityId)

        #we add isChampionPoint, which is a boolean
        urlString += "&IsChampionPoint="
        urlString += (str(isChampionPoint)).lower()

        #LevelMin and LevelMax
        urlString += "&LevelMin="
        urlString += levelMin
        urlString += "&LevelMax="
        urlString += levelMax

        #MasterWritVoucherMin and MasterWritVoucherMax
        urlString += "&MasterWritVoucherMin="
        urlString += masterWritVoucherMin
        urlString += "&MasterWritVoucherMax="
        urlString += masterWritVoucherMax

        #AmountMin and AmountMax
        urlString += "&AmountMin="
        urlString += amountMin
        urlString += "&AmountMax="
        urlString += amountMax

        #PriceMin and PriceMax
        urlString += "&PriceMin="
        urlString += priceMin
        urlString += "&PriceMax="
        urlString += priceMax

        #page
        urlString += "&page="
        urlString += page

        return urlString

a = UrlBuilder()
print(a.build("eu","pc","mother's sorrow","weapon","","inferno staff","nirnhoned","epic",bool(False),"50","","","","","","","25000",""))