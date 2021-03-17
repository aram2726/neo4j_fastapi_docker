from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .responses import JsonResponse
from src.app.infrastructure.controllers import APIController

app = FastAPI()


@app.route("/", methods=["GET"])
async def home(request):
    return JSONResponse(
        {"message": "Hello from neo4j and FastAPI."}
    )


@app.route("/customers", methods=["GET"])
async def all_customers(request):
    controller = APIController(request)
    data = await controller.list_customers()
    return JsonResponse(content=data)


@app.route("/customer/{key}/{condition}/{value}", methods=["GET"])
async def filter_customer(request):
    controller = APIController(request)
    data = await controller.get_customer(**request.path_params)
    return JsonResponse(content=data)


@app.route("/companies", methods=["GET"])
async def all_companies(request):
    controller = APIController(request)
    data = await controller.list_companies()
    return JsonResponse(content=data)


@app.route("/companies/{key}/{condition}/{value}", methods=["GET"])
async def filter_companies(request):
    controller = APIController(request)
    data = await controller.get_companies(**request.path_params)
    return JsonResponse(content=data)


@app.route("/countries", methods=["GET"])
async def all_countries(request):
    controller = APIController(request)
    data = await controller.list_countries()
    return JsonResponse(content=data)


@app.route("/countries/{key}/{condition}/{value}", methods=["GET"])
async def filter_countries(request):
    controller = APIController(request)
    data = await controller.get_countries(**request.path_params)
    return JsonResponse(content=data)


@app.route("/cities", methods=["GET"])
async def all_cities(request):
    controller = APIController(request)
    data = await controller.list_cities()
    return JsonResponse(content=data)


@app.route("/cities/{key}/{condition}/{value}", methods=["GET"])
async def filter_cities(request):
    controller = APIController(request)
    data = await controller.get_cities(**request.path_params)
    return JsonResponse(content=data)


@app.route("/graph-view", methods=["GET"])
async def show_graph(request):
    controller = APIController(request)
    data = await controller.get_graph_view()
    return JsonResponse(content=data)
