-- SELECT W.FULL_NAME, W.BADGE_ID, HIRE_DATE
-- FROM WORKDAY.V_WORKDAY_CURRENT_V2 W
-- WHERE W.TERMINATED = '0'
-- AND W.WORK_EMAIL_ADDRESS != 'NULL'
-- AND trunc(W.HIRE_DATE) < trunc(current_date)
-- and trunc(W.HIRE_DATE) >= trunc(current_date -7)
-- -- trunc(CURRENT_DATE)
--     AND (COST_CENTER_ID = '3400'
--          OR COST_CENTER_ID = '3470'
--          or COST_CENTER_ID = '3700')

-- --SNOWFLAKE
SELECT FULL_NAME, BADGE_ID, HIRE_DATE
FROM VSLR.HR.T_EMPLOYEE
WHERE TERMINATED = 0
AND WORK_EMAIL_ADDRESS != 'NULL'
AND HIRE_DATE < TRUNC(CURRENT_DATE, 'DAY' )
AND HIRE_DATE >= DATEADD(DAY, -7, CURRENT_DATE)
AND (COST_CENTER_ID = '3400'
      OR COST_CENTER_ID = '3470'
      OR COST_CENTER_ID = '3700')
ORDER BY HIRE_DATE DESC;