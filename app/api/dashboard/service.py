from sqlalchemy.orm import Session
from . import repository

def get_distributor_dashboard_stats(db: Session, distributor_id: int):
    orders = repository.get_distributor_orders(db=db, distributor_id=distributor_id)
    transactions = repository.get_distributor_transactions(db=db, distributor_id=distributor_id)

    total_sales = sum(order.amount for order in orders)
    total_commission = sum(transaction.commission_amount for transaction in transactions)
    number_of_orders = len(orders)

    return {
        "total_sales": total_sales,
        "total_commission": total_commission,
        "number_of_orders": number_of_orders,
    }
