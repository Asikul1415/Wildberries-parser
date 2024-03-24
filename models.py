from pydantic import BaseModel, root_validator

class Price(BaseModel):
    total: float
    basic: float   

    @root_validator(pre=True)
    def convert_price_to_rubles(cls, values: dict):
        price = values.get("total")
        basic = values.get("basic")
        if price is not None:
            values["total"] = price / 100
        if basic is not None:
            values["basic"] = basic / 100
        return values

class Size(BaseModel):
    price: Price

class Item(BaseModel):
    id: int
    brand: str
    brandId: int
    name: str
    supplier: str
    supplierId: int
    supplierRating: float
    reviewRating: float
    feedbacks: int
    volume: int
    sizes: list[Size]

class Items(BaseModel):
    products: list[Item]

 
