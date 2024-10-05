from pydantic import BaseModel


class CartModel(BaseModel):
    id: int
    sellerprice: "SellerPriceModel"
    quantity: int


class DiscountsModel(BaseModel):
    id: int
    percent: int


class ProductModel(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    one_discount: list[DiscountsModel]


class SellerPriceModel(BaseModel):
    id: int
    product: ProductModel
    count_products: int
    price: float
