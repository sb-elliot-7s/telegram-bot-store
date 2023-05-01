import grpc

import products_pb2 as pb2
import products_pb2_grpc as pb2_grpc
from products_service import ProductsService
from service_center_logic import ServiceCenterLogic


class ProductsServicer(pb2_grpc.ProductsServiceServicer):

    def __init__(self, product_service: ProductsService, geo_service_center_logic: ServiceCenterLogic):
        self.geo_service_center_logic = geo_service_center_logic
        self.product_service = product_service

    async def GetBrands(self, request, context: grpc.aio.ServicerContext):
        brands = await self.product_service.get_brands()
        return pb2.BrandsResponse(results=[pb2.Brand(**i) for i in brands])

    async def GetCategories(self, request, context):
        return pb2.CategoryResponse(results=[
            pb2.Category(**i) for i in await self.product_service.get_categories(brand=request.brand)
        ])

    async def Search(self, request, context: grpc.aio.ServicerContext):
        product = await self.product_service.search(title=request.product_name)
        if product is None:
            await context.abort(code=grpc.StatusCode.NOT_FOUND, details='Product not found')
        return pb2.ProductResponse(**product)

    async def GetSpecifications(self, request, context):
        result = await self.product_service.get_specifications(product_id=request.product_id)
        return pb2.SpecifiactionsResponse(result=result.get('result'))

    async def GetProduct(self, request, context):
        product = await self.product_service.product(product_id=request.product_id)
        return pb2.ProductResponse(**product)

    async def GetProducts(self, request, context):
        results = await self.product_service \
            .get_products(brand=request.brand, category=request.category, page=request.page)
        return pb2.ListProductsResponse(products=results)

    async def GetCount(self, request, context):
        count = await self.product_service.count_of_products(brand=request.brand, category=request.category)
        return pb2.ProductsCountResponse(products_count=count)

    async def GetServiceCenter(self, request, context: grpc.aio.ServicerContext):
        results = await self.geo_service_center_logic.get_service_center(city=request.city)
        return pb2.ServiceCenterListResponse(results=results)
