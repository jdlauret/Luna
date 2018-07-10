select t.service_name,
    c.full_name,
    c.email,
    t.service_address,
    t.service_city,
    t.service_state,
    t.service_zip_code
from sfrpt.t_dm_project t
inner join sfrpt.t_dm_contact c
    on c.contact_id = t.contract_signer
where t.service_number = :serviceNum;
SELECT DISTINCT P.SERVICE_NUMBER, ESC.ESC_SCHEDULED_FOR, NULL ARRAYS, D.SYSTEM_SIZE_DESIGNED_KW, D.MODULE_QTY, D.ROOF_TYPE, D.INVERTER_MANUFACTURER, D.INVERTER_MODEL, D.TOTAL_SOLAR_ROOFS, T.ROOF_TILT, T.ROOF_AZIMUTH_DESIGNED, T.NUM_MODULES_DESIGNED
FROM SFRPT.MV_CAD_ROOF_CONFIGURATIONS T
INNER JOIN SFRPT.T_DM_SYSTEM_DESIGN D ON T.SOLAR_CAD = D.CAD_ID
INNER JOIN SFRPT.T_DM_PROJECT P ON D.CAD_ID = P.PRIMARY_CAD
LEFT JOIN (SELECT * FROM SFRPT.T_DM_CASE C WHERE C.RECORD_TYPE = 'Solar - Electrical Service Change') ESC ON P.PROJECT_ID = ESC.PROJECT_ID
WHERE P.START_BILLING IS NULL
AND P.SERVICE_NUMBER = :serviceNum;