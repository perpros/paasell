from fastapi import FastAPI
from .api.users import views as user_views
from .api.admin import views as admin_views
from .api.dashboard import views as dashboard_views
from .api.campaigns import views as campaign_views
from .api.distributors import views as distributor_views
from .api.needs import views as need_views
from .api.orders import views as order_views
from .api.suppliers import views as supplier_views

app = FastAPI()

app.include_router(user_views.router, prefix="/api/v1/users", tags=["users"])
app.include_router(admin_views.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(dashboard_views.router, prefix="/api/v1", tags=["dashboard"])
app.include_router(campaign_views.router, prefix="/api/v1/campaigns", tags=["campaigns"])
app.include_router(distributor_views.router, prefix="/api/v1/distributor", tags=["distributor"])
app.include_router(need_views.router, prefix="/api/v1/needs", tags=["needs"])
app.include_router(order_views.router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(supplier_views.router, prefix="/api/v1/suppliers", tags=["suppliers"])
