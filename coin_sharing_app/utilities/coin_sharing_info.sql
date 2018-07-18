SELECT W.BADGE_ID,
      W.WORK_EMAIL_ADDRESS,
      W.FIRST_NAME,
      W.LAST_NAME
FROM WORKDAY.V_WORKDAY_CURRENT W
WHERE W.TERMINATED = '0'
AND W.WORK_EMAIL_ADDRESS != 'NULL'
AND W.SUPERVISOR_BADGE_ID_3 = '201322'
AND W.WORK_EMAIL_ADDRESS = :work_email_address;
