from ninja import NinjaAPI
from api_man.api.api1 import app as api1

app=NinjaAPI()
app.add_router('v1',api1)