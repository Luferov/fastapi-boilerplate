from fastapi import FastAPI
from fastapi.routing import APIRoute


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function names.

    Should be called only after all routes have been added.
    """
    unique_routes = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            assert route.name not in unique_routes, f'Route name {route.name} is duplicate'
            route.operation_id = route.name
            unique_routes.add(route.name)