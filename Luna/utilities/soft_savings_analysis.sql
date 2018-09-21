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
    m.record_type
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
left join mack_damavandi.t_utility_match x
    on upper(x.sf_utility_name) = upper(t.utility_company) and x.sf_state = t.service_state
inner join mack_damavandi.t_utility_rates_summary u
    on u.state = x.cm_state and upper(u.utility) = upper(x.cm_utility_name)
left join sfrpt.t_dm_contract m
    on t.primary_contract_id = m.contract_id
where t.service_number = :serviceNum
    and t.project_status != 'Cancelled'

;select to_char(t.read_date,'Mon YYYY') "Month Year",
    t.actual_kwh "Actual (kWh)",
    nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(t.read_date)-trunc(p.start_billing))/365)),t.current_rate_kwh),0) "PPA/Lease rate per kWh",
    round(t.actual_kwh*nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(t.read_date)-trunc(p.start_billing))/365)),t.current_rate_kwh),0),2) "Vivint Solar Bill",
    round(t.actual_kwh*coalesce(u.blended_rate,u.vslr_calculated_rate),2) "Utility Bill",
    round(t.actual_kwh*(coalesce(u.blended_rate,u.vslr_calculated_rate)-nvl(coalesce(p.rate_per_kwh*power(1.029,trunc((trunc(t.read_date)-trunc(p.start_billing))/365)),t.current_rate_kwh),0)),2) "Savings"
from fleet_production.mv_fusion_weather_adjusted t
inner join sfrpt.t_dm_project p
    on p.project_id = t.project_id
left join mack_damavandi.t_utility_match x
    on upper(x.sf_utility_name) = upper(p.utility_company) and x.sf_state = p.service_state
inner join mack_damavandi.t_utility_rates_summary u
    on u.state = x.cm_state and upper(u.utility) = upper(x.cm_utility_name)
where p.service_number = :serviceNum
    and t.read_date between to_date(:startDate,'MM/DD/YYYY') and to_date(:endDate,'MM/DD/YYYY')
    and t.lifetime_total_days = (select max(w.lifetime_total_days)
                                 from fleet_production.mv_fusion_weather_adjusted w
                                 where w.project_id = t.project_id
                                    and w.month = t.month
                                    and w.year = t.year)
order by t.read_date

-- -- SNOWFLAKE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- SELECT
--     T.SERVICE_NAME,
--     C.FULL_NAME,
--     C.EMAIL,
--     T.SERVICE_ADDRESS,
--     T.SERVICE_CITY,
--     T.SERVICE_STATE,
--     T.SERVICE_ZIP_CODE,
--     DATE_TRUNC('D', T.START_BILLING),
--     T.UTILITY_COMPANY,
--     U.BLENDED_RATE,
--     M.RECORD_TYPE
-- FROM VSLR.RPT.T_PROJECT AS T
-- INNER JOIN VSLR.RPT.T_CONTACT AS C ON C.CONTACT_ID = T.CONTRACT_SIGNER
-- LEFT JOIN VSLR.D_POST_INSTALL.T_UTILITY_MATCH AS X ON UPPER(X.SF_UTILITY_NAME) = UPPER(T.UTILITY_COMPANY) AND X.SF_STATE = T.SERVICE_STATE
-- INNER JOIN VSLR.D_POST_INSTALL.T_UTILITY_RATES_SUMMARY AS U ON U.STATE = X.CM_STATE AND UPPER(U.UTILITY) = UPPER(X.CM_UTILITY_NAME)
-- LEFT JOIN VSLR.RPT.T_CONTRACT AS M ON T.PRIMARY_CONTRACT_ID = M.CONTRACT_ID
-- WHERE T.PROJECT_STATUS != 'Cancelled'
-- AND T.SERVICE_NUMBER = :serviceNum;
--
-- SELECT *
-- FROM information_schema.columns
-- WHERE column_name ILIKE '%read_date%';
--
-- SELECT
--       TO_CHAR(T.READ_DATE, 'MON YYYY') AS "Month Year",
--       T.ACTUAL_KWH AS "Actual (kWh)",
--       NVL(COALESCE (P.RATE_PER_KWH * POWER(1.029,TRUNC(DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', T.READ_DATE)) / 365)), T.CURRENT_RATE_KWH), 0) AS "PPA/Lease rate per kWh",
--       ROUND(T.ACTUAL_KWH * NVL(COALESCE(P.RATE_PER_KWH * POWER(1.029, TRUNC(DATEDIFF('D', DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', T.READ_DATE)) / 365)),T.CURRENT_RATE_KWH), 0), 2) AS "Vivint Solar Bill",
--       ROUND(T.ACTUAL_KWH * COALESCE (U.BLENDED_RATE, U.VSLR_CALCULATED_RATE), 2) AS "Utility Bill",
--       ROUND(T.ACTUAL_KWH * (COALESCE (U.BLENDED_RATE, U.VSLR_CALCULATED_RATE) - NVL(COALESCE(P.RATE_PER_KWH * POWER(1.029, TRUNC((DATEDIFF(DAY, DATE_TRUNC('D', P.START_BILLING), DATE_TRUNC('D', T.READ_DATE))) / 365)), T.CURRENT_RATE_KWH), 0)), 2) AS "Savings"
-- FROM VSLR.FLEET.T_DAILY_ENERGY_WA AS T
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = T.PROJECT_ID
-- LEFT JOIN VSLR.D_POST_INSTALL.T_UTILITY_MATCH AS X ON UPPER(X.SF_UTILITY_NAME) = UPPER(P.UTILITY_COMPANY) AND X.SF_STATE = P.SERVICE_STATE
-- INNER JOIN VSLR.D_POST_INSTALL.T_UTILITY_RATES_SUMMARY AS U ON U.STATE = X.CM_STATE AND UPPER(U.UTILITY) = UPPER(X.CM_UTILITY_NAME)
-- WHERE T.LIFETIME_TOTAL_DAYS = (
--                               SELECT
--                                     MAX(W.LIFETIME_TOTAL_DAYS)
--                               FROM VSLR.FLEET.T_DAILY_ENERGY_WA AS W
--                               WHERE W.PROJECT_ID = T.PROJECT_ID
--                               AND W.MONTH = T.MONTH
--                               AND W.YEAR = T.YEAR
--                               )
-- AND P.SERVICE_NUMBER =:serviceNum
-- AND T.READ_DATE BETWEEN TO_DATE(:startDate, 'MM/DD/YYYY') AND TO_DATE(:endDate, 'MM/DD/YYYY')
-- ORDER BY T.READ_DATE