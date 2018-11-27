SELECT BADGE
     , NAME
     , SUPERVISOR
     , SUM(MIN_WORKED)        AS MIN_WORKED
     , SUM(BREAKS)            AS BREAKS
     , SUM(ACTIVITY_TIME)     AS ACTIVITY_TIME
     , SUM(TRAINING_TIME)     AS TRAINING_TIME
     , SUM(MEETING_TIME)      AS MEETING_TIME
     , SUM(NULL)              AS HUDDLE_TIME--Now that there is no huddle time it has to be nulled or it will throw an error.
     , SUM(PROJECT_TIME)      AS PROJECT_TIME
     , TO_VARCHAR(PREVIOUS_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'su'),
                  'MM/DD/YY') AS WEEK_STARTING
     , TO_VARCHAR(NEXT_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'sa'),
                  'MM/DD/YY') AS WEEK_ENDING
FROM VSLR.D_POST_INSTALL.V_SREC_AGENT_PRODUCTIVITY
WHERE DAYOFWEEK(REPORT_DATE) BETWEEN 1 AND 5
    AND REPORT_DATE BETWEEN Previous_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'su')
    AND PREVIOUS_DAY(DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ), 'su')
    AND METRIC_LEVEL = 'Employee'
    AND BADGE = '{badge}'
GROUP BY BADGE, NAME, SUPERVISOR, WEEK_START, WEEK_ENDING
ORDER BY NAME, WEEK_STARTING DESC;

-- SELECT BADGE,
--        NAME,
--        SUPERVISOR,
--        SUM(MIN_WORKED)                                                                                               AS MIN_WORKED,
--        SUM(BREAKS)                                                                                                   AS BREAKS,
--        SUM(ACTIVITY_TIME)                                                                                            AS ACTIVITY_TIME,
--        SUM(TRAINING_TIME)                                                                                            AS TRAINING_TIME,
--        SUM(MEETING_TIME)                                                                                             AS MEETING_TIME,
--        SUM(HUDDLE_TIME)                                                                                              AS HUDDLE_TIME,
--        SUM(PROJECT_TIME)                                                                                             AS PROJECT_TIME,
--        TO_VARCHAR(PREVIOUS_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'SU'),
--                   'MM/DD/YY')                                                                                        as REPORT_DATE1,
--        TO_VARCHAR(NEXT_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'sa'),
--                   'MM/DD/YY')                                                                                        AS REPORT_DATE2
-- FROM VSLR.D_POST_INSTALL.V_SREC_AGENT_PRODUCTIVITY
-- WHERE DAYOFWEEK(REPORT_DATE) BETWEEN 1 AND 5
--   AND REPORT_DATE BETWEEN Previous_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'su')
--           AND NEXT_DAY(DATEADD('d', -7, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)), 'sa')
--   AND BADGE = '{badge}'
-- GROUP BY BADGE, NAME, SUPERVISOR