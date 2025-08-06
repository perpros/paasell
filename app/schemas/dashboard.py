from pydantic import BaseModel

class DistributorDashboard(BaseModel):
    total_sales: float
    total_commission: float
    number_of_orders: int
