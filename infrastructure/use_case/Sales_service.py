import datetime
from logging import Logger
from uuid import UUID

from application.persistence.product_repo import ProductRepository
from application.persistence.sales_repo import SalesRepository
from application.persistence.stock_entry import StockEntryRepository
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.sale import CreateSaleRequest, CreateSaleResponse, VerifySaleResponse
from application.use_case.sales_service import SalesService as DefaultSaleService
from domain.models import Sale, SaleItem
from infrastructure.payment import PaystackService


class SaleService(DefaultSaleService):
    _logger: Logger
    sale_repository: SalesRepository
    product_repository: ProductRepository
    stock_repository: StockEntryRepository
    paystack_service: PaystackService

    def __init__(self, logger: Logger, sale_repository: SalesRepository, product_repository: ProductRepository, stock_repository: StockEntryRepository, paystack_service: PaystackService):
        self._logger = logger
        self._sale_repository = sale_repository
        self._product_repository = product_repository
        self._stock_entry = stock_repository
        self._paystack_service = paystack_service

    def create(self, user_id: UUID, email: str, sale: CreateSaleRequest) -> BaseResponse:
        self._logger.info(f"Creating sale ")
        total_amount = 0
        sale_items = []
        updates_to_stock = []

        for item in sale.items:
            product = self._product_repository.get(item.product_id)
            if not product:
                response = BaseResponse(status=False, message=f"Product {item.product_id} not found")
                response._status_code= 400
                return response

            sorted_stock = sorted(product.stock_entries, key=lambda s: s.added_date)

            total_available = sum(s.remaining_quantity for s in sorted_stock)
            if total_available < item.quantity:
                response = BaseResponse(status=False, message=f"Not enough stock for product {item.product_id}")
                response._status_code= 400
                return response

            quantity_to_fulfill = item.quantity
            for stock_entry in sorted_stock:
                if quantity_to_fulfill == 0:
                    break
                quantity_from_this_batch = min(quantity_to_fulfill, stock_entry.remaining_quantity)

                if quantity_from_this_batch > 0:
                    total_amount += quantity_from_this_batch * stock_entry.selling_price

                    sale_items.append(SaleItem(product_id=product.id, quantity=quantity_from_this_batch, sale_price=stock_entry.selling_price))

                    stock_entry.remaining_quantity -= quantity_from_this_batch
                    updates_to_stock.append(stock_entry)
                    quantity_to_fulfill -= quantity_from_this_batch

        amount_in_kobo = int(total_amount * 100)
        payment_response = self._paystack_service.initialize_transaction(email=email, amount_in_kobo=amount_in_kobo)
        if not payment_response:
            self._logger.error(f"Paystack transaction failed")
            response = BaseResponse(status=False, message=f"Payment failed")
            response._status_code= 400
            return response
        payment_data = payment_response["data"]
        reference = payment_data["reference"]

        new_sale = Sale(customer_id=user_id, sale_date=datetime.datetime.now(datetime.timezone.utc), total_amount=total_amount, paid=False, payment_reference=reference, items=sale_items )
        created_sale = self._sale_repository.create(new_sale)
        if not created_sale:
            self._logger.error(f"Failed to create sale {created_sale.id}")
            response = BaseResponse(status=False, message=f"Failed to create sale {created_sale.id}")
            response._status_code= 500
            return response
        self._logger.info(f"Created sale {created_sale.id}")
        stock_reduction = self._stock_entry.reduce_stock_for_sales(entries_to_reduce=updates_to_stock)
        if not stock_reduction:
            self._logger.error(f"Failed to reduce stock for sale {created_sale.id}")
        response = CreateSaleResponse(status=True, authorization_url=payment_data["authorization_url"], access_code=payment_data["access_code"], reference=reference)
        response._status_code = 200
        return response


    def verify_payment(self, reference: str) -> BaseResponse:
        verification_data = self._paystack_service.verify_transaction(reference)

        if not verification_data:
            self._logger.error(f"Paystack verification failed")
            response = BaseResponse(status=False, message="Payment verification failed with gateway.")
            response._status_code= 400
            return response


        sale = self._sale_repository.get_by_reference(reference)
        if not sale:
            response =  BaseResponse(status=False, message="Sale not found for this reference.")
            response._status_code= 400
            return response

        if sale.paid:
            self._logger.error(f"Sale has already been verified")
            response = VerifySaleResponse(status=True, message="Payment has already been verified.", sale_id=sale.id, payment_status="success")
            response._status_code= 200
            return response

        sale.paid = True
        self._sale_repository.update(sale=sale)

        self._logger.info(f"Payment verified and sale finalized for reference: {reference}")
        response =  VerifySaleResponse(
            status=True,
            message="Payment successful and sale finalized.",
            sale_id=sale.id,
            payment_status=verification_data["data"].get("status")
        )
        response._status_code = 200
        return response