from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ... import dependencies, models
from ...schemas import dashboard as dashboard_schema
from . import service

router = APIRouter()

@router.get(
    "/distributor/dashboard",
    response_model=dashboard_schema.DistributorDashboard
)
def distributor_dashboard(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.role_checker([models.Role.distributor]))
):
    """
    Retrieve sales and profit statistics for the current distributor.
    """
    dashboard_data = service.get_distributor_dashboard_stats(db=db, distributor_id=current_user.id)
    return dashboard_data
