SELECT
      T.SERVICE_NAME,
      INITCAP(C.FULL_NAME),
      C.PHONE,
      INITCAP(C.EMAIL),
      INITCAP(T.SERVICE_ADDRESS),
      INITCAP(T.SERVICE_CITY),
      T.SERVICE_STATE,
      T.SERVICE_ZIP_CODE
FROM VSLR.RPT.T_PROJECT AS T
INNER JOIN VSLR.RPT.T_CONTACT AS C
      ON C.CONTACT_ID = T.CONTRACT_SIGNER
      WHERE T.SERVICE_NUMBER = '{service_number}';

SELECT
    -- For now, Brescia is okay with just listing tilt and azimuth for all roof sections, comma-separated
    -- Long-term, she'd like it to reflect the roof sections listed in the Roof Section(s) field of the Removal Case (currently missing from t_case)
    -- Currently, that field is a mess. Brescia will work with Aubree to see if a Salesforce solution can help standardize that field.
    -- If we ever do look at specific roof sections, we'll need access to a Roof Section table (e.g., a view to SF.SOLAR_ROOF__C)
    -- Roof sections can be named or numbered. They display on the Primary CAD in alphabetical order (so section 3 would be the third section alphabetically)
    --     If this ever happens, make sure SQL's alphabetization is matching Salesforce's (watch out that SQL alphabetizes all uppercase before all lowercase)
       em.supervisory_org
      , ca.case_number
      , pr.roc_name
      , pr.pto_awarded IS NOT NULL AS is_post_pto
      , pr.service_number -- Might want service_name instead
      , pr.service_name
      , cad.system_size_actual_kw
      , NVL(cad.total_modules_actual, cad.total_modules_designed) AS total_modules
      , ca.requested_modules_to_be_removed
      , ca.partial_or_complete
      , rc.roof_tilt AS tilt
      , rc.roof_azimuth AS azimuth
      , NVL(cad.inverter_manufacturer, pr.backend_provider) AS inverter
      , ca.racking_type
      , cad.module_manufacturer
      , cad.module_model
FROM rpt.t_case ca
INNER JOIN vslr.HR.t_employee em on ca.CREATED_BY_EMPLOYEE_ID = em.badge_id
INNER JOIN rpt.t_project pr ON  ca.project_id = pr.project_id
INNER JOIN rpt.t_cad cad
    -- Brescia said to use Primary CAD if possible, and to fall back to Proposal CAD if Primary CAD is missing
    -- The logic that populates T_PROJECT already takes care of this (PRIMARY_CAD is set to PROPOSAL_CAD if it is blank)
ON  pr.primary_cad = cad.cad_id
-- Left instead of INNER because some CADs don't have any roof sections listed
LEFT OUTER JOIN rpt.v_cad_roof_configurations rc ON  pr.primary_cad = rc.cad_id
WHERE ca.record_type = 'Solar - Panel Removal'
AND PR.SERVICE_NUMBER = '{service_number}';