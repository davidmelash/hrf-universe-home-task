import argparse
import sys
from sqlalchemy import text
from db import get_session

UPSERT_FROM_VIEW = """
INSERT INTO public.days_to_hire_stats (
    standard_job_id,
    country_code,
    min_days_to_hire,
    max_days_to_hire,
    avg_days_to_hire,
    job_postings_count
)
SELECT
    standard_job_id,
    country_code,
    min_days_to_hire,
    max_days_to_hire,
    avg_days_to_hire,
    job_postings_count
FROM public.job_posting_stats_view
WHERE job_postings_count >= :min_job_postings
ON CONFLICT (standard_job_id, country_code)
DO UPDATE SET
    min_days_to_hire = EXCLUDED.min_days_to_hire,
    max_days_to_hire = EXCLUDED.max_days_to_hire,
    avg_days_to_hire = EXCLUDED.avg_days_to_hire,
    job_postings_count = EXCLUDED.job_postings_count;
"""


def calculate_stats(min_job_postings: int):
    session = get_session()
    try:
        with session.begin():
            session.execute(text(UPSERT_FROM_VIEW), {"min_job_postings": min_job_postings})
        print("Statistics calculated and stored successfully.")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(
        description="Calculate and store days-to-hire statistics"
    )
    parser.add_argument(
        "--min-job-postings",
        type=int,
        default=5,
        help=(
            "Minimum number of job postings"
            "Default is 5"
        ),
    )
    args = parser.parse_args()
    calculate_stats(args.min_job_postings)


if __name__ == "__main__":
    main()
