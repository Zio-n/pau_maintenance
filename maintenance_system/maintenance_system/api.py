from ninja import NinjaAPI
from shift_schedule.api import shift_router

api = NinjaAPI()

api.add_router('/shift/',shift_router)