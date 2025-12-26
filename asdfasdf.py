from fastapi import FastAPI, HTTPException, status
from typing import Optional


app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3,
                   sample_product_4, sample_product_5]


@app.get('/product/{product_id}')
async def get_product_by_id(product_id: int):
    for i in sample_products:
        if i['product_id'] == product_id:
            return i
    return {'msg': 'продукт с таким id не найден'}


@app.get('/products/search')
async def get_product_by_filter(
    keyword: str,
    category: Optional[str] = None,
    limit: Optional[int] = 10
):
    result = []
    for i in sample_products:
        dict_values = list(i.values())
        dict_values = [str(value).lower() for value in dict_values]
        if isinstance(category, int):
            if keyword.lower() in dict_values and category.lower() in dict_values:
                result.append(i)
        elif keyword.lower() in dict_values:
            result.append(i)
    if len(result):
        return result[:limit]
    else:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail='Не было найдено ни одного продукта')

        raise HTTPException
