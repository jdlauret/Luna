SELECT W.FULL_NAME
FROM WORKDAY.V_WORKDAY_CURRENT_V2 W
WHERE W.TERMINATED = '0'
AND W.WORK_EMAIL_ADDRESS != 'NULL'
and (W.SUPERVISOR_BADGE_ID_1 = 201869
          OR W.SUPERVISOR_BADGE_ID_2 = 201869
          OR W.SUPERVISOR_BADGE_ID_3 = 201869
          OR W.SUPERVISOR_BADGE_ID_4 = 201869
          OR W.SUPERVISOR_BADGE_ID_5 = 201869
          OR W.SUPERVISOR_BADGE_ID_6 = 201869
          OR W.SUPERVISOR_BADGE_ID_7 = 201869
          OR W.SUPERVISOR_BADGE_ID_8 = 201869
          OR W.SUPERVISOR_BADGE_ID_9 = 201869
          OR W.SUPERVISOR_BADGE_ID_10 = 201869)
AND W.BADGE_ID = :badge_id;