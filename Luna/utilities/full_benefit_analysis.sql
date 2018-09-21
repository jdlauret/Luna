select t.service_name,
     c.full_name,
     c.email,
     t.service_address,
     t.service_city,
     t.service_state,
     t.service_zip_code,
     trunc(t.start_billing),
     t.utility_company,
     u.blended_rate,
     sd.current_annual_energy_consumpt
 from sfrpt.t_dm_project t
 inner join sfrpt.t_dm_contact c
     on c.contact_id = t.contract_signer
 left join mack_damavandi.t_utility_rates u
     on upper(u.utility) = upper(t.utility_company) and u.state = t.service_state
 left join sfrpt.t_dm_system_design sd
     on sd.cad_id = t.primary_cad
where t.service_number = :serviceNum

;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.actual_kwh "Actual (kWh)",
    round(t.actual_kwh*nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(p.start_billing)-trunc(sysdate))/365)),
                                    t.current_rate_kwh),0),2) "Vivint Solar Bill"
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
left join mack_damavandi.t_utility_rates u
    on upper(u.utility) = upper(p.utility_company) and u.state = p.service_state
where p.service_number = :serviceNum
    and t.read_date between to_date(:startDate,'MM/DD/YYYY') and to_date(:endDate,'MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet_production.mv_fusion_weather_adjusted w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date
--
-- -- -- SNOWFLAKE CONVERSION
--
-- SELECT
--       P.SERVICE_NAME,
--       C.FULL_NAME,
--       P.SERVICE_ADDRESS,
--       P.SERVICE_CITY,
--       P.SERVICE_STATE,
--       P.SERVICE_ZIP_CODE,
--       DATE_TRUNC('D', P.START_BILLING),
--       P.UTILITY_COMPANY,
--       U.BLENDED_RATE,
--       CAD.CURRENT_ANNUAL_ENERGY_CONSUMPTION
-- FROM VSLR.RPT.T_PROJECT AS P
-- INNER JOIN VSLR.RPT.T_CONTACT AS C ON C.CONTACT_ID = P.CONTRACT_SIGNER
-- LEFT JOIN VSLR.D_POST_INSTALL.T_UTILITY_RATES AS U ON UPPER(U.UTILITY) = UPPER(P.UTILITY_COMPANY) AND U.STATE = P.SERVICE_STATE
-- LEFT JOIN VSLR.RPT.T_CAD AS CAD ON CAD.CAD_ID = P.PRIMARY_CAD
-- WHERE P.SERVICE_NUMBER = :serviceNum;
--
-- SELECT
--     TO_VARCHAR(T.READ_DATE, 'Mon YYYY') AS MONTH_YEAR,
--     T.ACTUAL_KWH,
--     ROUND(T.ACTUAL_KWH * NVL(COALESCE (P.RATE_PER_KWH * POWER(1.029, TRUNC(DATEDIFF('D', DATE_TRUNC('D', P.START_BILLING),DATE_TRUNC('D', CURRENT_TIMESTAMP::TIMESTAMP_NTZ))/365)), T.CURRENT_RATE_KWH), 0), 2) AS VIVINT_SOLAR_BILL
-- FROM VSLR.FLEET.T_DAILY_ENERGY_WA AS T
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = T.PROJECT_ID
-- LEFT JOIN VSLR.D_POST_INSTALL.T_UTILITY_RATES_SUMMARY AS U ON UPPER(U.UTILITY) = UPPER(P.UTILITY_COMPANY)
--           AND U.STATE = P.SERVICE_STATE
-- WHERE P.SERVICE_NUMBER = :serviceNum
-- AND T.READ_DATE BETWEEN TO_DATE(:startDate, 'MM/DD/YYYY') AND TO_DATE(:endDate,'MM/DD/YYYY')
-- AND T.LIFETIME_TOTAL_DAYS = (SELECT MAX(W.LIFETIME_TOTAL_DAYS) FROM VSLR.FLEET.T_DAILY_ENERGY_WA AS W WHERE W.PROJECT_ID = T.PROJECT_ID AND W.MONTH = T.MONTH AND W.YEAR = T.YEAR)
-- ORDER BY T.READ_DATE;