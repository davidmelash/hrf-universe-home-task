from fastapi import FastAPI, Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy import select

from home_task.db import get_session
from sqlalchemy.orm import Session

from home_task.models import DaysToHireStats

app = FastAPI()


class DaysToHireStatsResponse(BaseModel):
    id: int
    standard_job_id: str
    country_code: str
    avg_days_to_hire: float
    min_days_to_hire: int
    max_days_to_hire: int
    job_postings_count: int

    class Config:
        orm_mode = True


@app.get("/api/v1/jobs", response_model=DaysToHireStatsResponse)
def read_item(standard_job_id: str, country_code: str = "WORLD", session: Session = Depends(get_session)):
    try:
        print(standard_job_id)
        print(country_code)
        query = select(DaysToHireStats).where(
            DaysToHireStats.standard_job_id == standard_job_id,
            DaysToHireStats.country_code == country_code
        )

        result = session.execute(query).scalar_one_or_none()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Not found for job ID {standard_job_id} in {country_code}"
            )

        return result

    except Exception:
        raise HTTPException(status_code=500, detail=f"Something went wrong")
    finally:
        session.close()