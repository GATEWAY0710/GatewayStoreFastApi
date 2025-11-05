from logging import Logger
from uuid import UUID

from application.persistence.product_repo import ProductRepository
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.product import CreateProductResponse, GetResponse, List, CreateProduct
from application.use_case.models.product import UpdateProduct
from application.use_case.models.stock_entry import GetStockResponse
from application.use_case.product_service import ProductService as DefaultProductService
from domain.models import Product


class ProductService(DefaultProductService):
    _logger: Logger
    _product_repository: ProductRepository

    def __init__(self, logger: Logger, product_repository: ProductRepository):
        self._logger = logger
        self._product_repository = product_repository

    def create(self, product: CreateProduct) -> BaseResponse:
        self._logger.info(f"adding product {product.name} ")
        product_exist = self._product_repository.get_by_name(product.name)
        if product_exist:
            self._logger.warning(f"{product.name} already exist in the database")
            response = BaseResponse(status=False, message=f"{product.name} already exist in database")
            response._status_code = 400
            return response

        product = Product(name=product.name, description=product.description, image=product.image)
        product = self._product_repository.create(product)
        if not product:
            self._logger.error(f"error adding {product.name}")
            response = BaseResponse(status=False, message=f"error adding {product.name}")
            response._status_code = 500
            return response
        self._logger.info(f"{product.name} added to database succesfully")
        response = CreateProductResponse(status=True, name=product.name, description=product.description, image=product.image)
        response._status_code = 200
        return response


    def update(self, name: str, product: UpdateProduct ) -> BaseResponse:
        product_exist = self._product_repository.get_by_name(name=name)
        if not product_exist:
            self._logger.warning(f"{name} does not exist in database")
            response = BaseResponse(status=False, message=f"{name} does not exist in database")
            response._status_code = 400
            return response
        product_exist.description = product.description
        product_exist.image = product.image

        product_update = self._product_repository.update(name=product_exist.name, product=product_exist)
        if not product_update:
            self._logger.error(f"error updating {product_exist.name} in database")
            response = BaseResponse(status= False, message=f"error updating {product_exist.name} in database")
            response._status_code = 500
            return response
        self._logger.info(f"{product_exist.name} updated succesfully")
        response = CreateProductResponse(status=True, name=product_exist.name, description=product_exist.description, image=product_exist.image)
        response._status_code = 200
        return response

    def get(self, id: UUID) -> BaseResponse:
        product_exist = self._product_repository.get(id=id)
        if not product_exist:
            self._logger.warning(f"product not in database")
            response = BaseResponse(status=False, message=f"product not in database")
            response._status_code = 400
            return response

        stock_items = []
        for stock in product_exist.stock_entries:
            stock_item = GetStockResponse(
                status=True,
                quantity=stock.quantity,
                cost_price=stock.cost_price,
                selling_price=stock.selling_price,
                added_date=str(stock.added_date),
                remaining_quantity=stock.remaining_quantity

            )
            stock_items.append(stock_item)

        self._logger.info(f"{product_exist.name} details below")
        response = GetResponse(status=True, id=product_exist.id, name=product_exist.name, description=product_exist.description, stock_items=stock_items, image=product_exist.image)
        response._status_code = 200
        return response


    def get_by_name(self, name: str) -> BaseResponse:
        product_exist = self._product_repository.get_by_name(name)
        if not product_exist:
            self._logger.warning(f"product not in database")
            response = BaseResponse(status=False, message="product not in database")
            response._status_code = 400
            return response

        stock_items = []
        for stock in product_exist.stock_entries:
            stock_item = GetStockResponse(
                status=True,
                quantity=stock.quantity,
                cost_price=stock.cost_price,
                selling_price=stock.selling_price,
                added_date=str(stock.added_date),
                remaining_quantity=stock.remaining_quantity

            )
            stock_items.append(stock_item)

        self._logger.info(f"{product_exist.name} deatils below")
        response = GetResponse(status=True, id=product_exist.id, name=product_exist.name, description=product_exist.description, stock_items=stock_items, image=product_exist.image)
        response._status_code = 200
        return response

    def list(self) -> BaseResponse:
        products = self._product_repository.list()
        products_dbs = []
        for product in products:
            stock_items = []
            remaining_quantity = 0
            for stock in product.stock_entries:
                remaining_quantity +=stock.remaining_quantity
                stock_item = GetStockResponse(
                    status=True,
                    quantity=stock.quantity,
                    cost_price=stock.cost_price,
                    selling_price=stock.selling_price,
                    added_date=str(stock.added_date),
                    remaining_quantity=remaining_quantity
                )
                stock_items.append(stock_item)
            product_list  = GetResponse(status=True, id=product.id ,name=product.name, description=product.description, stock_items=stock_items, image=product.image)
            products_dbs.append(product_list)

        self._logger.info("list of products below")
        response = List(status=True, products=products_dbs)
        response._status_code = 200
        return response