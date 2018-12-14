SELECT
  wd.supervisor_badge_id_1
  , wd.supervisor_name_1
FROM
    hr.t_employee wd
WHERE
    wd.mgr_id_3 = 209122 -- Chuck Browne
AND wd.mgr_id_4 IN (120220, 104550, 200023, 207208, 210253) -- Carissa, Kelsey, Kristen, Tali, Robert
AND wd.terminated = 0
AND wd.pay_rate_type = 'Hourly'
AND wd.is_people_manager = 0
AND wd.business_title NOT ILIKE '%Supervisor%' -- Sometimes new supervisors slip past is_people_manager because they don't have any subordinates yet
AND REGEXP_REPLACE(wd.supervisory_org, ' *\\([^\\)]*\\(.*\\)$', '') NOT IN ('Business Analytics', 'Call & Workflow Quality Control', 'Click Support', 'Default Managers', 'Executive Resolutions', 'Meter Readers (East)', 'Project Specialists', 'Training', 'Workforce Management')
ORDER BY
    wd.supervisor_name_1
;

