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

SELECT
      P.SERVICE_NUMBER,
      D.SYSTEM_SIZE_ACTUAL,
       D.REMAINING_CONTRACT_TERM
FROM SFRPT.MV_SYSTEM_DETAILS D
INNER JOIN SFRPT.T_DM_PROJECT P ON D.PROJECT_NAME = P.PROJECT_NAME
WHERE P.SERVICE_NUMBER = :serviceNum;
