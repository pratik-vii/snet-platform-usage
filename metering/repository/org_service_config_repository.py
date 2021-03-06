from models import OrgServiceConfigModel
from repository.base_repository import BaseRepository


class OrgServiceRepo(BaseRepository):

    def get_service_config(self, org_id, service_id, optin_time):
        session = self.get_default_session()
        if optin_time is not None:
            service_config = session.query(OrgServiceConfigModel.free_calls.label('free_calls')) \
                .filter(OrgServiceConfigModel.org_id == org_id) \
                .filter(OrgServiceConfigModel.service_id == service_id) \
                .filter(OrgServiceConfigModel.effective_start_date <= optin_time) \
                .filter(OrgServiceConfigModel.effective_end_date >= optin_time).all()
        else:
            service_config = session.query(OrgServiceConfigModel.free_calls.label('free_calls')) \
                .filter(OrgServiceConfigModel.org_id == org_id) \
                .filter(OrgServiceConfigModel.service_id == service_id) \
                .order_by(OrgServiceConfigModel.created_at.desc()).all()
        session.commit()
        session.flush()
        if len(service_config) == 0:
            return None
        return service_config[0].free_calls
