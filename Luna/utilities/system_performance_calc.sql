select t.service_name,
    c.full_name,
    c.email,
    t.service_address,
    t.service_city,
    t.service_state,
    t.service_zip_code,
    trunc(t.start_billing)
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
where t.service_number = :serviceNum
    and t.project_status != 'Cancelled'

;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.estimated_kwh "Design Estimates",
    nvl(t.estimated_corrected_kwh, t.estimated_kwh) "Weather Corrected Estimate",
    t.actual_kwh "Actual",
    round(t.actual_kwh/t.estimated_kwh,4) "Design Performance",
    nvl(round(t.performance_ratio,4), round(t.actual_kwh/nvl(t.estimated_corrected_kwh, t.estimated_kwh),4)) "Weather Corrected Performance" --t.actual_kwh/t.estimated_corrected_kwh
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
where p.service_number = :serviceNum
    and t.read_date between to_date(:startDate,'MM/DD/YYYY') and to_date(:endDate,'MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet_production.mv_fusion_weather_adjusted w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date;

-- -- SNOWFLAKE CONVERSION ***************************************************************************************
-- SELECT
--       P.SERVICE_NAME,
--       CO.FULL_NAME,
--       CO.EMAIL,
--       P.SERVICE_ADDRESS,
--       P.SERVICE_CITY,
--       P.SERVICE_STATE,
--       P.SERVICE_ZIP_CODE,
--       TRUNC(P.START_BILLING, 'DAY')
-- FROM VSLR.RPT.T_PROJECT AS P
-- INNER JOIN VSLR.RPT.T_CONTACT AS CO ON CO.CONTACT_ID = P.CONTRACT_SIGNER
-- WHERE P.PROJECT_STATUS != 'Cancelled'
-- AND P.SERVICE_NUMBER = :serviceNum;
--
-- SELECT
--       TO_CHAR(E.READ_DATE, 'Mon YYYY') AS "Month Year",
--       E.ESTIMATED_KWH AS "Design Estimates",
--       NVL(E.ESTIMATED_CORRECTED_KWH, E.ESTIMATED_KWH) AS "Weather Corrected Estimate",
--       E.ACTUAL_KWH AS "Actual",
--       ROUND(E.ACTUAL_KWH/E.ESTIMATED_KWH, 4) AS "Design Performance",
--       NVL(ROUND(E.PERFORMANCE_RATIO, 4),
--       ROUND (E.ACTUAL_KWH/ NVL(E.ESTIMATED_CORRECTED_KWH, E.ESTIMATED_KWH), 4)) AS "Weather Corrected Performance"
-- FROM VSLR.FLEET.T_DAILY_ENERGY_WA AS E
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = E.PROJECT_ID
-- WHERE E.LIFETIME_TOTAL_DAYS = (
--                           SELECT
--                                 MAX(L.LIFETIME_TOTAL_DAYS)
--                                 FROM FLEET.T_DAILY_ENERGY_WA AS L
--                                 WHERE L.PROJECT_ID = E.PROJECT_ID
--                                 AND L.MONTH = E.MONTH
--                                 AND L.YEAR = E.YEAR
--                           )
-- AND P.SERVICE_NUMBER = :serviceNum
-- AND E.READ_DATE BETWEEN TO_DATE(:startDate, 'MM/DD/YYYY') AND TO_DATE(:endDate, 'MM/DD/YYYY')
-- ORDER BY E.READ_DATE;