SELECT
    wd.full_name
  , wd.badge_id
  , wd.business_title
  , wd.supervisor_badge_id_1
  , wd.supervisor_name_1
  , CASE
        WHEN wd.business_title LIKE 'Central Scheduling - %'
        THEN 'Central Scheduling'
        WHEN wd.business_title LIKE 'Customer Relations - %'
        THEN 'Customer Relations'
        WHEN wd.business_title LIKE 'Customer Service - %'
        THEN 'Customer Service'
        WHEN wd.business_title LIKE 'Customer Solutions - %'
        THEN 'Customer Solutions'
        WHEN wd.business_title LIKE 'RECs ' || CHR(38) || ' Rebates - %'
        THEN 'RECs ' || CHR(38) || ' Rebates'
        WHEN wd.business_title LIKE 'Resolution - %'
        THEN 'Resolution'
        WHEN wd.business_title LIKE 'Transfer - %'
        THEN 'Transfer'
        ELSE 'Other'
    END AS team
  , CASE
        WHEN wd.business_title LIKE 'Central Scheduling - Inbound %'
        THEN 'Inbound'
        WHEN wd.business_title LIKE 'Central Scheduling - Auxiliary %'
        THEN 'Auxiliary'
        WHEN wd.business_title LIKE 'Central Scheduling - Super Agent %'
        THEN 'Super Agent'
        WHEN wd.business_title LIKE 'Central Scheduling - Service %'
        THEN 'Service'
        WHEN wd.business_title LIKE 'Customer Solutions - Admin %'
        THEN 'Admin'
        WHEN wd.business_title LIKE 'Customer Relations - Inbound/Outbound %'
        THEN 'Inbound/Outbound'
        WHEN wd.business_title LIKE 'Customer Relations - Email Admin %'
        THEN 'Email Admin'
        WHEN wd.business_title LIKE 'Customer Relations - Documents %'
        THEN 'Documents'
    END AS subteam
  , CASE
        WHEN wd.business_title LIKE '% - Rep 1%'
        THEN 'Representative 1'
        WHEN wd.business_title LIKE '% - Rep 2%'
        THEN 'Representative 2'
        WHEN wd.business_title LIKE '% - Rep 3%'
        THEN 'Representative 3'
        WHEN wd.business_title LIKE '% - Specialist 1%'
        THEN 'Specialist 1'
        WHEN wd.business_title LIKE '% - Specialist 2%'
        THEN 'Specialist 2'
        WHEN wd.business_title LIKE '% - Specialist 3%'
        THEN 'Specialist 3'
        WHEN wd.business_title LIKE '% - Team Lead%'
        THEN 'Team Lead'
    END AS tier
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
    wd.full_name
;
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
GROUP BY
wd.SUPERVISOR_BADGE_ID_1,
wd.SUPERVISOR_NAME_1
ORDER BY
wd.SUPERVISOR_NAME_1
;