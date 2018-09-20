select t.service_name,
    c.full_name,
    c.email,
    t.service_address,
    t.service_city,
    t.service_state,
    t.service_zip_code,
    t.START_BILLING
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
where t.service_number = :serviceNum;

SELECT DISTINCT P.SERVICE_NUMBER, to_char(nvl(ESC.ESC_SCHEDULED_FOR,esc.upgrade_scheduled_for), 'Mon DD, YYYY HH24:MI:SS')esc_scheduled_for,
                NULL ARRAYS,
                D.SYSTEM_SIZE_DESIGNED_KW,
                D.MODULE_QTY,
                D.ROOF_TYPE,
                D.INVERTER_MANUFACTURER,
                D.INVERTER_MODEL,
                D.TOTAL_SOLAR_ROOFS,
                T.ROOF_TILT,
                T.ROOF_AZIMUTH_DESIGNED,
                T.NUM_MODULES_DESIGNED
FROM SFRPT.MV_CAD_ROOF_CONFIGURATIONS T
INNER JOIN SFRPT.T_DM_SYSTEM_DESIGN D ON T.SOLAR_CAD = D.CAD_ID
INNER JOIN SFRPT.T_DM_PROJECT P ON D.CAD_ID = P.PRIMARY_CAD
LEFT JOIN (SELECT * FROM SFRPT.T_DM_CASE C WHERE C.RECORD_TYPE = 'Solar - Electrical Service Change') ESC ON P.PROJECT_ID = ESC.PROJECT_ID
WHERE P.SERVICE_NUMBER = :serviceNum;

-- --SNOWFLAKE
-- SELECT T.SERVICE_NAME,
--       C.FULL_NAME,
--       C.EMAIL,
--       T.SERVICE_ADDRESS,
--       T.SERVICE_CITY,
--       T.SERVICE_STATE,
--       T.SERVICE_ZIP_CODE,
--       T.START_BILLING
-- FROM VSLR.RPT.T_PROJECT AS T
-- INNER JOIN VSLR.RPT.T_CONTACT AS C
--       ON C.CONTACT_ID = T.CONTRACT_SIGNER
-- WHERE T.SERVICE_NUMBER = :serviceNum;
--
-- SELECT DISTINCT
--         P.SERVICE_NUMBER,
--         TO_CHAR(NVL(ESC.ESC_SCHEDULED_FOR, ESC.UPGRADE_SCHEDULED_FOR),'Mon DD, YYYY HH24:MI:SS') ESC_SCHEDULED_FOR,
--         NULL ARRAYS,
--         C.SYSTEM_SIZE_DESIGNED_KW,
--         C.MODULE_QTY,
--         C.ROOF_TYPE,
--         C.INVERTER_MANUFACTURER,
--         C.INVERTER_MODEL,
--         C.TOTAL_SOLAR_ROOFS,
--         I.TILT,
--         CO.AZIMUTH,
--         C.TOTAL_MODULES_DESIGNED
-- FROM VSLR.RPT.T_CAD AS C
-- INNER JOIN VSLR.RPT.T_PROJECT AS P ON C.CAD_ID = P.PRIMARY_CAD
-- LEFT JOIN VSLR.RPT.T_IDM AS I ON P.SERVICE_NUMBER = I.SERVICE_NUMBER
-- LEFT JOIN (SELECT * FROM VSLR.RPT.T_CASE AS C WHERE C.RECORD_TYPE = 'Solar - Electrical Service Change') AS ESC ON P.PROJECT_ID = ESC.PROJECT_ID
-- LEFT JOIN VSLR.COBBLESTONE.V_PAY_LOAD_ROOF_SECTION AS CO ON P.SERVICE_NUMBER = CO.SERVICE
-- WHERE P.SERVICE_NUMBER = :serviceNum;