CREATE OR REPLACE VIEW public.job_posting_stats_view AS
WITH per_country_stats AS (
    SELECT
        p.standard_job_id,
        p.country_code,
        CAST(p.lower_bound AS int) AS min_days_to_hire,
        CAST(p.upper_bound AS int) AS max_days_to_hire,
        AVG(j.days_to_hire)::float AS avg_days_to_hire,
        COUNT(*) AS job_postings_count
    FROM (
        SELECT
            standard_job_id,
            country_code,
            percentile_cont(0.1) WITHIN GROUP (ORDER BY days_to_hire) AS lower_bound,
            percentile_cont(0.9) WITHIN GROUP (ORDER BY days_to_hire) AS upper_bound
        FROM public.job_posting
        WHERE days_to_hire IS NOT NULL
          AND country_code IS NOT NULL
        GROUP BY standard_job_id, country_code
    ) p
    JOIN public.job_posting j
      ON j.standard_job_id = p.standard_job_id
     AND j.country_code = p.country_code
     AND j.days_to_hire BETWEEN p.lower_bound AND p.upper_bound
    GROUP BY p.standard_job_id, p.country_code, p.lower_bound, p.upper_bound
),
world_stats AS (
    SELECT
        p.standard_job_id,
        'WORLD' AS country_code,
        CAST(p.lower_bound AS int) AS min_days_to_hire,
        CAST(p.upper_bound AS int) AS max_days_to_hire,
        AVG(j.days_to_hire)::float AS avg_days_to_hire,
        COUNT(*) AS job_postings_count
    FROM (
        SELECT
            standard_job_id,
            percentile_cont(0.1) WITHIN GROUP (ORDER BY days_to_hire) AS lower_bound,
            percentile_cont(0.9) WITHIN GROUP (ORDER BY days_to_hire) AS upper_bound
        FROM public.job_posting
        WHERE days_to_hire IS NOT NULL
        GROUP BY standard_job_id
    ) p
    JOIN public.job_posting j
      ON j.standard_job_id = p.standard_job_id
     AND j.days_to_hire BETWEEN p.lower_bound AND p.upper_bound
    GROUP BY p.standard_job_id, p.lower_bound, p.upper_bound
)
SELECT * FROM per_country_stats
UNION ALL
SELECT * FROM world_stats;
