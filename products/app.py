import asyncio
from typing import Any

import grpc

import products_pb2_grpc as pb2_grpc
from db import category_collection, brand_collection, products_collection, service_center_collection
from grpc_server import ProductsServicer
from products_service import ProductsService
from repository import ProductRepository
from service_center_logic import ServiceCenterLogic
from service_center_repository import ServiceCenterRepository


def get_services() -> dict[str, Any]:
    db_collections = {
        'brand_collection': brand_collection,
        'category_collection': category_collection,
        'products_collection': products_collection
    }
    return {
        'product_service': ProductsService(repository=ProductRepository(**db_collections)),
        'geo_service_center_logic': ServiceCenterLogic(
            repository=ServiceCenterRepository(collection=service_center_collection))
    }


async def run_server():
    server = grpc.aio.server(compression=grpc.Compression.Gzip)
    services = get_services()
    pb2_grpc.add_ProductsServiceServicer_to_server(servicer=ProductsServicer(**services), server=server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(run_server())
