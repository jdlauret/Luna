SELECT T.SERVICE_NAME,
      C.FULL_NAME,
      C.EMAIL,
      T.SERVICE_ADDRESS,
      T.SERVICE_CITY,
      T.SERVICE_STATE,
      T.SERVICE_ZIP_CODE,
      T.START_BILLING
FROM VSLR.RPT.T_PROJECT AS T
INNER JOIN VSLR.RPT.T_CONTACT AS C
      ON C.CONTACT_ID = T.CONTRACT_SIGNER
      WHERE T.SERVICE_NUMBER = '{service_number}';


WITH CAD1  AS--All CAD Columns
    (SELECT C.SYSTEM_SIZE_DESIGNED_KW
          , C.MODULE_QTY
          , C.ROOF_TYPE
          , C.INVERTER_MANUFACTURER
          , C.INVERTER_MODEL
          , C.TOTAL_SOLAR_ROOFS
          , c.PROJECT_ID
          , c.CAD_ID
          , c.CAD_DESIGN_COMPLETED
          , row_number() OVER (PARTITION BY c.PROJECT_ID ORDER BY c.CAD_DESIGN_COMPLETED DESC)AS rn
     FROM VSLR.RPT.T_CAD AS C)
   , CAD2  AS--Filter Unique PROJECT_ID
    (SELECT * FROM CAD1 WHERE CAD1.rn = 1)
   , CASE1 AS--All Case Columns
    (SELECT ca.*, row_number() OVER (PARTITION BY ca.PROJECT_ID ORDER BY ca.CREATED_DATE DESC)AS rn
     FROM VSLR.RPT.T_CASE AS CA
     WHERE Ca.RECORD_TYPE = 'Solar - Electrical Service Change'
         AND
           CA.STATUS != 'Closed')
   , CASE2 AS--Filtering unique Project_ID
    (SELECT * FROM CASE1 WHERE CASE1.rn = 1)
   , IDM1  AS (SELECT idm.ARRAYS
                    , idm.PROJECT_ID
                    , idm.STATUS_DATE
                    , row_number() OVER (PARTITION BY idm.PROJECT_ID ORDER BY idm.STATUS_DATE DESC)AS rn
               FROM VSLR.RPT.T_IDM idm)
   , IDM2  AS (SELECT * FROM IDM1 WHERE IDM1.rn = 1)
   , ROOF1 AS (SELECT ROOF.ROOF_TILT, ROOF.ROOF_AZIMUTH, ROOF.NUM_MODULES_DESIGNED, Roof.CAD_id
               FROM VSLR.RPT.V_CAD_ROOF_CONFIGURATIONS ROOF
               ORDER BY ROOF.CAD_ID)
   , T1    AS--Main Query
    (SELECT P.SERVICE_NUMBER
          , TO_CHAR(NVL(ESC.ESC_SCHEDULED_FOR, ESC.UPGRADE_SCHEDULED_FOR),
                    'Mon DD, YYYY HH24:MI:SS')                                           AS ESC_SCHEDULED_FOR
          , I.ARRAYS
          , C.SYSTEM_SIZE_DESIGNED_KW
          , C.MODULE_QTY
          , C.ROOF_TYPE
          , C.INVERTER_MANUFACTURER
          , C.INVERTER_MODEL
          , C.TOTAL_SOLAR_ROOFS
          , ROOF.ROOF_TILT
          , ROOF.ROOF_AZIMUTH
          , ROOF.NUM_MODULES_DESIGNED
          , row_number() OVER (PARTITION BY p.PROJECT_ID ORDER BY esc.created_date DESC) AS RN
     FROM VSLR.RPT.T_PROJECT p
              LEFT JOIN CAD2 AS C
              ON C.CAD_ID = P.PRIMARY_CAD
              LEFT JOIN IDM2 AS I
              ON P.project_id = I.project_id
              LEFT JOIN CASE2 ESC
              ON P.PROJECT_ID = ESC.PROJECT_ID
              LEFT JOIN ROOF1 AS ROOF
              ON P.PRIMARY_CAD = ROOF.CAD_ID)

SELECT T1.SERVICE_NUMBER
     , T1.ESC_SCHEDULED_FOR
     , T1.ARRAYS
     , T1.SYSTEM_SIZE_DESIGNED_KW
     , T1.MODULE_QTY
     , T1.ROOF_TYPE
     , T1.INVERTER_MANUFACTURER
     , T1.INVERTER_MODEL
     , T1.TOTAL_SOLAR_ROOFS
     , T1.ROOF_TILT
     , T1.ROOF_AZIMUTH
     , T1.NUM_MODULES_DESIGNED
FROM T1
WHERE T1.SERVICE_NUMBER = '{service_number}';