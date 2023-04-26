from schemas import ProductSchema


async def get_specification_util(product_schema: ProductSchema):
    result_message = []
    for key, value in product_schema.dict(exclude_none=True, exclude={'id'}).items():
        descr = product_schema.schema().get('properties').get(key).get('description')
        if descr is not None:
            res = f'{descr}: {value}\n'
            result_message.append(res)
    return ''.join(result_message)
