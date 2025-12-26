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


@app.get('/products/search')
async def get_product_by_filter(
    keyword: str,
    category: Optional[str],
    limit: Optional[int] = 10
):
    result = []
    keyword_lower = keyword.lower()

    for product in sample_products:
        name_contains_keyword = keyword_lower in product["name"].lower()

        if category:
            category_matches = category.lower() == product["category"].lower()
            if name_contains_keyword and category_matches:
                result.append(product)
        else:
            if name_contains_keyword:
                result.append(product)

    limited_result = result[:limit]

    if not limited_result:
        error_detail = f"Не найдено товаров по запросу '{keyword}'"
        if category:
            error_detail += f" в категории '{category}'"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_detail
        )

    return limited_result
