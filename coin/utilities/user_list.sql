SELECT W.BADGE_ID, W.FULL_NAME
FROM WORKDAY.V_WORKDAY_CURRENT_V2 W
WHERE W.TERMINATED = '0'
AND W.WORK_EMAIL_ADDRESS != 'NULL'
    AND (COST_CENTER_ID = '3400'
         OR COST_CENTER_ID = '3470'
         or COST_CENTER_ID = '3700')
ORDER BY W.FULL_NAME;

-- Back up query on coin_sharing_app_status table
-- select rownum, W.FULL_NAME, W.BADGE_ID
-- from workday.V_WORKDAY_CURRENT_V2 W
-- WHERE W.TERMINATED = '0'
-- and BADGE_ID= 201869;
--
-- INSERT INTO JDLAURET.COIN_SHARING_APP_STATUS (ID, NAME, BADGEID, GIVE, TOTAL, CREATE_AT, EDITED)
-- select rownum, W.FULL_NAME, W.BADGE_ID, 0, 0, sysdate, sysdate
-- from workday.V_WORKDAY_CURRENT_V2 W
-- WHERE W.TERMINATED = '0'
-- and (W.SUPERVISOR_BADGE_ID_1 = 201869
--           OR W.SUPERVISOR_BADGE_ID_2 = 201869
--           OR W.SUPERVISOR_BADGE_ID_3 = 201869
--           OR W.SUPERVISOR_BADGE_ID_4 = 201869
--           OR W.SUPERVISOR_BADGE_ID_5 = 201869
--           OR W.SUPERVISOR_BADGE_ID_6 = 201869
--           OR W.SUPERVISOR_BADGE_ID_7 = 201869
--           OR W.SUPERVISOR_BADGE_ID_8 = 201869
--           OR W.SUPERVISOR_BADGE_ID_9 = 201869
--           OR W.SUPERVISOR_BADGE_ID_10 = 201869);
--
-- INSERT INTO JDLAURET.COIN_SHARING_APP_STATUS (ID, NAME, BADGEID, GIVE, TOTAL, CREATE_AT, EDITED)
-- VALUES (293, 'Bryce Barnett', 201869, 0, 0, sysdate, sysdate);
--
-- commit ;