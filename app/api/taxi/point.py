from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from typing import List

from domain.taxi.point.persistance.point_query_dao import MongoDBPointQueryDao
from src.taxi_container import TaxiContainer

point_router = APIRouter(prefix='/point')


class PointModel(BaseModel):
    id: str = Field(..., description='포인트 ID', examples=['ObjectId'])
    name: str = Field(..., description='포인트 이름', examples=['부산대학교 밀양캠퍼스'])


@point_router.get('', response_model=List[PointModel], tags=['point'])
@inject
async def get_points(point_query: MongoDBPointQueryDao = Depends(Provide[TaxiContainer.point_query_dao])):
    points = point_query.find_points()
    return [point.json for point in points]
