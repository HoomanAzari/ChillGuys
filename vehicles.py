import json


class Vehicle:

    def __init__(self, json_object):
        self.Type = json_object["Type"]
        self.Stock = json_object["Stock"]
        self.VIN = json_object["VIN"]
        self.Year = json_object["Year"]
        self.Make = json_object["Make"]
        self.Model = json_object["Model"]
        self.Body = json_object["Body"]
        self.ModelNumber = json_object["ModelNumber"]
        self.Doors = json_object["Doors"]
        self.ExteriorColor = json_object["ExteriorColor"]
        self.InteriorColor = json_object["InteriorColor"]
        self.EngineCylinders = json_object["EngineCylinders"]
        self.EngineDisplacement = json_object["EngineDisplacement"]
        self.Transmission = json_object["Transmission"]
        self.Miles = json_object["Miles"]
        self.SellingPrice = json_object["SellingPrice"]
        self.MSRP = json_object["MSRP"]
        self.BookValue = json_object["BookValue"]
        self.Invoice = json_object["Invoice"]
        self.Certified = json_object["Certified"]
        self.Options = json_object["Options"]
        self.Style_Description = json_object["Style_Description"]
        self.Ext_Color_Generic = json_object["Ext_Color_Generic"]
        self.Ext_Color_Code = json_object["Ext_Color_Code"]
        self.Int_Color_Generic = json_object["Int_Color_Generic"]
        self.Int_Color_Code = json_object["Int_Color_Code"]
        self.Int_Upholstery = json_object["Int_Upholstery"]
        self.Engine_Block_Type = json_object["Engine_Block_Type"]
        self.Engine_Aspiration_Type = json_object["Engine_Aspiration_Type"]
        self.Engine_Description = json_object["Engine_Description"]
        self.Transmission_Speed = json_object["Transmission_Speed"]
        self.Transmission_Description = json_object["Transmission_Description"]
        self.Drivetrain = json_object["Drivetrain"]
        self.Fuel_Type = json_object["Fuel_Type"]
        self.CityMPG = json_object["CityMPG"]
        self.HighwayMPG = json_object["HighwayMPG"]
        self.EPAClassification = json_object["EPAClassification"]
        self.Wheelbase_Code = json_object["Wheelbase_Code"]
        self.Internet_Price = json_object["Internet_Price"]
        self.MarketClass = json_object["MarketClass"]
        self.PassengerCapacity = json_object["PassengerCapacity"]
        self.ExtColorHexCode = json_object["ExtColorHexCode"]
        self.IntColorHexCode = json_object["IntColorHexCode"]
        self.EngineDisplacementCubicInches = json_object[
            "EngineDisplacementCubicInches"]

    @staticmethod
    def get_objects(path_to_json: str) -> list[type("Vehicle")]:
        with open(path_to_json, "r") as fp:
            json_obj = json.load(fp)
        vehicles = []
        for obj in json_obj:
            new_vehicle = Vehicle(obj)
            vehicles.append(new_vehicle)
        return vehicles


def main():
    vehicles = Vehicle.get_objects("vehicles.json")
    print(vehicles[1].Options)
    print(vehicles.__len__())


if __name__ == "__main__":
    main()
