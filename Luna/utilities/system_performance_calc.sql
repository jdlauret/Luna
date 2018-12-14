SELECT
      P.SERVICE_NAME,
      CO.FULL_NAME,
      CO.EMAIL,
      P.SERVICE_ADDRESS,
      P.SERVICE_CITY,
      P.SERVICE_STATE,
      P.SERVICE_ZIP_CODE,
      DATE_TRUNC('D', P.START_BILLING)
FROM VSLR.RPT.T_PROJECT AS P
INNER JOIN VSLR.RPT.T_CONTACT AS CO ON CO.CONTACT_ID = P.CONTRACT_SIGNER
WHERE P.PROJECT_STATUS != 'Cancelled'
AND P.SERVICE_NUMBER = '{service_number}';

SELECT
      TO_CHAR(E.READ_DATE, 'Mon YYYY') AS "Month Year",
      E.ESTIMATED_KWH AS "Design Estimates",
      NVL(E.ESTIMATED_CORRECTED_KWH, E.ESTIMATED_KWH) AS "Weather Corrected Estimate",
      E.ACTUAL_KWH AS "Actual",
      ROUND(E.ACTUAL_KWH/E.ESTIMATED_KWH, 4) AS "Design Performance",
      NVL(ROUND(E.PERFORMANCE_RATIO, 4),
      ROUND (E.ACTUAL_KWH/ NVL(E.ESTIMATED_CORRECTED_KWH, E.ESTIMATED_KWH), 4)) AS "Weather Corrected Performance"
FROM VSLR.FLEET.T_DAILY_ENERGY_WA AS E
INNER JOIN VSLR.RPT.T_PROJECT AS P ON P.PROJECT_ID = E.PROJECT_ID
WHERE E.LIFETIME_TOTAL_DAYS = (
                          SELECT
                                MAX(L.LIFETIME_TOTAL_DAYS)
                                FROM FLEET.T_DAILY_ENERGY_WA AS L
                                WHERE L.PROJECT_ID = E.PROJECT_ID
                                AND L.MONTH = E.MONTH
                                AND L.YEAR = E.YEAR
                          )
AND P.SERVICE_NUMBER = '{service_number}'
AND E.READ_DATE BETWEEN TO_DATE('{start_date}', 'MM/DD/YYYY') AND TO_DATE('{end_date}', 'MM/DD/YYYY')
ORDER BY E.READ_DATE;