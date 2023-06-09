# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import products_pb2 as products__pb2


class ProductsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBrands = channel.unary_unary(
                '/ProductsService/GetBrands',
                request_serializer=products__pb2.BrandRequest.SerializeToString,
                response_deserializer=products__pb2.BrandsResponse.FromString,
                )
        self.GetCategories = channel.unary_unary(
                '/ProductsService/GetCategories',
                request_serializer=products__pb2.CategoryRequest.SerializeToString,
                response_deserializer=products__pb2.CategoryResponse.FromString,
                )
        self.Search = channel.unary_unary(
                '/ProductsService/Search',
                request_serializer=products__pb2.ProductSearchRequest.SerializeToString,
                response_deserializer=products__pb2.ProductResponse.FromString,
                )
        self.GetSpecifications = channel.unary_unary(
                '/ProductsService/GetSpecifications',
                request_serializer=products__pb2.ProductRequest.SerializeToString,
                response_deserializer=products__pb2.SpecifiactionsResponse.FromString,
                )
        self.GetProduct = channel.unary_unary(
                '/ProductsService/GetProduct',
                request_serializer=products__pb2.ProductRequest.SerializeToString,
                response_deserializer=products__pb2.ProductResponse.FromString,
                )
        self.GetProducts = channel.unary_unary(
                '/ProductsService/GetProducts',
                request_serializer=products__pb2.ProductsRequest.SerializeToString,
                response_deserializer=products__pb2.ListProductsResponse.FromString,
                )
        self.GetCount = channel.unary_unary(
                '/ProductsService/GetCount',
                request_serializer=products__pb2.ProductsCountRequest.SerializeToString,
                response_deserializer=products__pb2.ProductsCountResponse.FromString,
                )
        self.GetServiceCenter = channel.unary_unary(
                '/ProductsService/GetServiceCenter',
                request_serializer=products__pb2.ServiceCenterRequest.SerializeToString,
                response_deserializer=products__pb2.ServiceCenterListResponse.FromString,
                )


class ProductsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetBrands(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCategories(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Search(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSpecifications(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProducts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServiceCenter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProductsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBrands': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBrands,
                    request_deserializer=products__pb2.BrandRequest.FromString,
                    response_serializer=products__pb2.BrandsResponse.SerializeToString,
            ),
            'GetCategories': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCategories,
                    request_deserializer=products__pb2.CategoryRequest.FromString,
                    response_serializer=products__pb2.CategoryResponse.SerializeToString,
            ),
            'Search': grpc.unary_unary_rpc_method_handler(
                    servicer.Search,
                    request_deserializer=products__pb2.ProductSearchRequest.FromString,
                    response_serializer=products__pb2.ProductResponse.SerializeToString,
            ),
            'GetSpecifications': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSpecifications,
                    request_deserializer=products__pb2.ProductRequest.FromString,
                    response_serializer=products__pb2.SpecifiactionsResponse.SerializeToString,
            ),
            'GetProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProduct,
                    request_deserializer=products__pb2.ProductRequest.FromString,
                    response_serializer=products__pb2.ProductResponse.SerializeToString,
            ),
            'GetProducts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProducts,
                    request_deserializer=products__pb2.ProductsRequest.FromString,
                    response_serializer=products__pb2.ListProductsResponse.SerializeToString,
            ),
            'GetCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCount,
                    request_deserializer=products__pb2.ProductsCountRequest.FromString,
                    response_serializer=products__pb2.ProductsCountResponse.SerializeToString,
            ),
            'GetServiceCenter': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServiceCenter,
                    request_deserializer=products__pb2.ServiceCenterRequest.FromString,
                    response_serializer=products__pb2.ServiceCenterListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ProductsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProductsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetBrands(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetBrands',
            products__pb2.BrandRequest.SerializeToString,
            products__pb2.BrandsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCategories(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetCategories',
            products__pb2.CategoryRequest.SerializeToString,
            products__pb2.CategoryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Search(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/Search',
            products__pb2.ProductSearchRequest.SerializeToString,
            products__pb2.ProductResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSpecifications(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetSpecifications',
            products__pb2.ProductRequest.SerializeToString,
            products__pb2.SpecifiactionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetProduct',
            products__pb2.ProductRequest.SerializeToString,
            products__pb2.ProductResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProducts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetProducts',
            products__pb2.ProductsRequest.SerializeToString,
            products__pb2.ListProductsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetCount',
            products__pb2.ProductsCountRequest.SerializeToString,
            products__pb2.ProductsCountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServiceCenter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ProductsService/GetServiceCenter',
            products__pb2.ServiceCenterRequest.SerializeToString,
            products__pb2.ServiceCenterListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
