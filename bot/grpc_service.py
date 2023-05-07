from dataclasses import dataclass

import grpc
from google.protobuf.json_format import MessageToDict

import products_pb2 as pb2
import products_pb2_grpc as pb2_grpc
from configs import get_configs
from constants import convert_category
from schemas import Brand, Category, ProductResponseSchema, ServiceCenterSchema


@dataclass
class GRPCProductsClient:
    host: str = get_configs().grpc_host
    port: int = 50051

    async def get_brands(self):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            message = pb2.BrandRequest(value='brand')
            results = await stub.GetBrands(message)
            return [Brand(id=x.id, value=x.name.title()) for x in results.results]

    async def get_categories(self, brand: str):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            message = pb2.CategoryRequest(brand=brand)
            results = await stub.GetCategories(message)
            return [Category(id=x.id, name=x.name, brand=x.brand) for x in results.results]

    async def get_products(self, brand: str, category: str, page: int | None = None):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            category = convert_category(category=category)
            if category:
                message_products = pb2.ProductsRequest(brand=brand.lower(), category=category, page=page)
                message_count = pb2.ProductsCountRequest(brand=brand.lower(), category=category)
                result = await stub.GetProducts(message_products)
                count = await stub.GetCount(message_count)
                return ProductResponseSchema(count_documents=count.products_count, products=result.products)

    async def get_specifications(self, product_id: int):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            message = pb2.ProductRequest(product_id=product_id)
            result = await stub.GetSpecifications(message)
            return result.result

    async def get_product(self, product_id: str):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            message = pb2.ProductRequest(product_id=product_id)
            return await stub.GetProduct(message)

    async def search(self, product_name: str):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            message = pb2.ProductSearchRequest(product_name=product_name)
            try:
                return await stub.Search(message)
            except grpc.aio.AioRpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    return None

    async def get_service_center(self, city: str):
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', compression=grpc.Compression.Gzip) as channel:
            stub = pb2_grpc.ProductsServiceStub(channel=channel)
            message = pb2.ServiceCenterRequest(city=city)
            results = await stub.GetServiceCenter(message)
            return [ServiceCenterSchema(**MessageToDict(i)) for i in results.results]
