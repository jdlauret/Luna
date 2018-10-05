WITH W1  AS                                                      -- Employee Info
    (SELECT WD.FULL_NAME            AS NAME
          , to_char(WD.EMPLOYEE_ID) AS BADGE
          , WD.SUPERVISOR_NAME_1    AS SUPERVISOR
          , WD.WORK_EMAIL_ADDRESS   AS AGENT_EMAIL
          , WD.BUSINESS_TITLE
     FROM HR.T_EMPLOYEE WD
     WHERE WD.MGR_ID_4 = '104550'
         AND
           WD.TERMINATED = 0
         AND
           WD.BUSINESS_TITLE NOT LIKE '%Supervisor%'
         AND
           WD.BUSINESS_TITLE NOT LIKE '%Project%')
--
                                                                 --
   , PT1 AS                                                      -- Non-Activity Times
    (SELECT DATE_TRUNC('d', PT.REPORT_DATE)                                                AS REPORT_DATE
          , PT.AGENT_EMAIL                                                                 AS AGENT_EMAIL
          , IFF(PT.TRAINING = 0, NULL, SUM(PT.TRAINING))                                   AS SUM_TRAINING
          , IFF(PT.MEETING = 0, NULL, SUM(PT.MEETING))                                     AS SUM_MEETING
          , IFF(PT.HUDDLE = 0, NULL, SUM(PT.HUDDLE))                                       AS SUM_HUDDLE
          , IFF(PT.NON_ACTIVITY_PROJECT_TIME = 0, NULL, SUM(PT.NON_ACTIVITY_PROJECT_TIME)) AS SUM_PROJECT_TIME
     FROM D_POST_INSTALL.T_SREC_PROJECT_TIMES PT
     WHERE DATE_TRUNC('d', PT.REPORT_DATE) >= DATEADD('d', -104, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ))
     GROUP BY DATE_TRUNC('d', PT.REPORT_DATE), PT.AGENT_EMAIL, PT.TRAINING, PT.MEETING, PT.HUDDLE
            , PT.NON_ACTIVITY_PROJECT_TIME)
--
                                                                 --
   , W2  AS (SELECT DATE_TRUNC('d', WDT.REPORTED_DATE)                                         AS REPORTED_DATE
                  , WDT.EMPLOYEE_ID                                                            AS BADGE
                  , W1.NAME
                  , W1.AGENT_EMAIL
                  , W1.SUPERVISOR
                  , ROUND((DATEDIFF('m', WDT.IN_TIME, WDT.OUT_TIME)), 2)                       AS MIN_WORKED
                  , ROUND((DATEDIFF('m', WDT.IN_TIME, WDT.OUT_TIME)) / 60, 2)                  AS HOURS_WORKED
                  , TRUNC(ROUND((((DATEDIFF('m', WDT.IN_TIME, WDT.OUT_TIME)) / 60) / 4) * 15)) AS BREAK_TIME
             FROM HR.V_EMPLOYEE_TIME_RPT WDT
                      INNER JOIN W1
                      ON W1.BADGE = WDT.EMPLOYEE_ID
             WHERE DATE_TRUNC('d', WDT.REPORTED_DATE) >=
                   DATE_TRUNC('d', DATEADD('d', -104, CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)) AND
                   wdt.CALCULATION_TAGS = 'Hourly')
                                                                 -----------------------------------
                                                                 --
                                                                 --
   , W3  AS                                                      -- Workday Main
    (SELECT DATE_TRUNC('d', W2.REPORTED_DATE) AS REPORT_DATE
          , W2.BADGE
          , W2.NAME
          , W2.SUPERVISOR
          , W2.AGENT_EMAIL
          , ROUND(SUM(W2.MIN_WORKED), 2)      AS MIN_WORKED
          , ROUND(SUM(W2.BREAK_TIME), 2)      AS BREAK_TIME
          , PT1.SUM_TRAINING                  AS SUM_TRAINING
          , PT1.SUM_MEETING                   AS SUM_MEETING
          , PT1.SUM_HUDDLE                    AS SUM_HUDDLE
          , PT1.SUM_PROJECT_TIME              AS SUM_PROJECT_TIME
     FROM W2
              LEFT JOIN PT1 -- Non-Activity Project Time
              ON PT1.AGENT_EMAIL = W2.AGENT_EMAIL AND
                 DATE_TRUNC('d', PT1.REPORT_DATE) = DATE_TRUNC('d', W2.REPORTED_DATE)
     WHERE DATE_TRUNC('d', W2.REPORTED_DATE) >= DATE_TRUNC('d', DATEADD('d', -104, CURRENT_TIMESTAMP :: TIMESTAMP_NTZ))
     GROUP BY DATE_TRUNC('d', W2.REPORTED_DATE), W2.BADGE, W2.NAME, W2.SUPERVISOR, W2.AGENT_EMAIL, PT1.SUM_TRAINING
            , PT1.SUM_HUDDLE, PT1.SUM_PROJECT_TIME, PT1.SUM_MEETING)
--
    /*  Select * from W3
   WHERE w3.BADGE = 112597
   ORDER BY W3.REPORT_DATE DESC;*/
--
   , A1  AS                                                      -- Activity Raw
    (SELECT DATE_TRUNC('d', T.CREATED_DATE)           AS REPORT_DATE
          , T.CREATED_BY                              AS NAME
          , T.CREATED_BY_EMPLOYEE_ID                  AS BADGE
          , T.SUBJECT
          , P.SERVICE_STATE                           AS STATE
          , P.PROJECT_ID
          , IFF(BT.BASE_TIME = 0, NULL, BT.BASE_TIME) AS BASE_TIME
     FROM RPT.T_TASK T
              INNER JOIN RPT.T_PROJECT P
              ON T.WHAT_ID = P.PHASE_ID
              INNER JOIN W1
              ON W1.BADGE = T.CREATED_BY_EMPLOYEE_ID
              INNER JOIN D_POST_INSTALL.T_SREC_ACTIVITY_BASE_TIMES BT
              ON BT.SUBJECT = T.SUBJECT AND
                 BT.STATE = P.SERVICE_STATE
     WHERE DATE_TRUNC('d', T.CREATED_DATE) >= DATEADD('d', -104, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ))
         AND
           T.SUBJECT NOT LIKE 'Call %'
         AND
           T.SUBJECT NOT LIKE 'RTS-%'
         AND
           T.CREATED_BY_EMPLOYEE_ID IS NOT NULL)
--
    /*Select COUNT(case when a1.BASE_TIME IS NULL  THEN a1.SUBJECT END) NULL_COUNT,
           COUNT(case when a1.BASE_TIME IS NOT NULL  THEN a1.SUBJECT END) COUNT
           *
    from A1 WHERE a1.NAME = 'Reanna Willardson' ORDER BY a1.REPORT_DATE DESC,a1.subject, a1.BADGE,  a1.PROJECT_ID;*/
--
   , A2  AS                                                      -- Team Specific Activities and Times
    (SELECT A1.REPORT_DATE, A1.BADGE, A1.SUBJECT, A1.BASE_TIME FROM A1)
--
                                                                 --
   , A3  AS (SELECT A2.REPORT_DATE
                  , A2.BADGE
                  , SUM(A2.BASE_TIME)                                             AS SUM_BASE_TIME
                  , COUNT(A2.BADGE)                                               AS TOTAL_COUNT
                  , COUNT(CASE WHEN A2.BASE_TIME IS NOT NULL THEN A2.SUBJECT END) AS ACTIVITIES
                  , COUNT(CASE WHEN A2.BASE_TIME IS NULL THEN A2.SUBJECT END)     AS ZERO_TIME_ACTIVITIES
             FROM A2
             GROUP BY A2.REPORT_DATE, A2.BADGE)
--
                                                                 --
   , E1  AS                                                      -- Error Tracker Raw
    (SELECT DATE_TRUNC('d', ER.ERROR_DATE) AS ERROR_DATE
          , ER.ERROR_BY
          , CASE WHEN ER.ERROR_1 IS NOT NULL
                      THEN 1
            END AS ERROR_1C
          , CASE WHEN ER.ERROR_2 IS NOT NULL
                      THEN 1
            END AS ERROR_2C
          , CASE WHEN ER.ERROR_3 IS NOT NULL
                      THEN 1
            END AS ERROR_3C
          , CASE WHEN ER.ERROR_4 IS NOT NULL
                      THEN 1
            END AS ERROR_4C
     FROM D_POST_INSTALL.T_SREC_ERROR_TRACKER ER
     WHERE DATE_TRUNC('d', ER.REPORT_DATE) >= DATEADD('d', -104, DATE_TRUNC('d', CURRENT_TIMESTAMP :: TIMESTAMP_NTZ)))
--
                                                                 --
   , E2  AS                                                      -- Error Tracker Aggregate
    (SELECT E1.ERROR_DATE, E1.ERROR_BY, NVL(SUM(E1.ERROR_1C), 0) + NVL(SUM(E1.ERROR_2C), 0) +
                                        NVL(SUM(E1.ERROR_3C), 0) + NVL(SUM(E1.ERROR_4C), 0) AS ERROR_COUNT
     FROM E1
     GROUP BY E1.ERROR_DATE, E1.ERROR_BY)
--
                                                                 --
   , E3  AS (SELECT E2.*, CASE WHEN AVG(E2.ERROR_COUNT) > 0
                                    THEN SUM(E2.ERROR_COUNT)
                          END AS SUM_ERROR_COUNT
             FROM E2
             GROUP BY E2.ERROR_DATE, E2.ERROR_BY, E2.ERROR_COUNT)--Check the error_count grouping.
                                                                 --
                                                                 --
   , M1  AS                                                      -- Metrics by Employee & Date Worked
    (SELECT W3.BADGE
          , W3.NAME
          , W3.SUPERVISOR
          , W3.AGENT_EMAIL
          , W3.REPORT_DATE
          , W3.MIN_WORKED
          , W3.BREAK_TIME                                 AS Breaks
          , A3.SUM_BASE_TIME                              AS ACTIVITY_TIME
          , W3.SUM_TRAINING                               AS TRAINING_TIME
          , W3.SUM_MEETING                                AS MEETING_TIME
          , W3.SUM_HUDDLE                                 AS HUDDLE_TIME
          , W3.SUM_PROJECT_TIME                           AS PROJECT_TIME
          , (NVL(A3.SUM_BASE_TIME, 0) + NVL(W3.SUM_TRAINING, 0) +
             NVL(W3.SUM_MEETING, 0) + NVL(W3.SUM_HUDDLE, 0) +
             NVL(W3.SUM_PROJECT_TIME, 0) + W3.BREAK_TIME) AS NUMERATOR
          , (W3.MIN_WORKED)                               AS DENOMINATOR
          , A3.ACTIVITIES                                 AS ACTIVITY_COUNT
          , E3.SUM_ERROR_COUNT                            AS ERROR_COUNT
          , A3.ZERO_TIME_ACTIVITIES                       AS ZERO_TIME_ACTIVITIES
     FROM W3 -- Workday Time Main
              LEFT JOIN A3 -- Activity Main
              ON A3.BADGE = W3.BADGE AND
                 A3.REPORT_DATE = W3.REPORT_DATE
              LEFT JOIN E3 -- Error Main
              ON E3.ERROR_BY = W3.NAME AND
                 E3.ERROR_DATE = W3.REPORT_DATE)
--
                                                                 --
   , M2  AS                                                      -- Additional columns
    (SELECT -- 6 Weeks
         M1.*, CASE WHEN M1.REPORT_DATE >= DATE_TRUNC('d', DATEADD('WEEK', -6, CURRENT_TIMESTAMP :: TIMESTAMP_NTZ))
                         THEN 'Yes'
                         ELSE 'No'
               END AS LAST_6_WEEKS, Previous_DAY(M1.REPORT_DATE, 'SUN') AS WEEK_START
     FROM M1)
--
                                                                 --
   , M3  AS                                                      -- Employee Level
    (SELECT M2.*, CAST('Employee' AS VARCHAR2(50)) AS METRIC_LEVEL FROM M2)
--
                                                                 --
   , M4  AS                                                      -- Team Wide Level
    (SELECT M2.BADGE
          , M2.NAME
          , M2.SUPERVISOR
          , M2.AGENT_EMAIL
          , M2.REPORT_DATE
          , ROUND(AVG(M2.MIN_WORKED) OVER (PARTITION BY M2.REPORT_DATE), 2)     AS MINUTES_WORKED
          , ROUND(AVG(M2.Breaks) OVER (PARTITION BY M2.REPORT_DATE), 2)         AS BREAKS
          , ROUND(AVG(M2.ACTIVITY_TIME) OVER (PARTITION BY M2.REPORT_DATE), 2)  AS ACTIVITY_TIME
          , ROUND(AVG(M2.TRAINING_TIME) OVER (PARTITION BY M2.REPORT_DATE), 2)  AS TRAINING_TIME
          , ROUND(AVG(M2.MEETING_TIME) OVER (PARTITION BY M2.REPORT_DATE), 2)   AS MEETING_TIME
          , ROUND(AVG(M2.HUDDLE_TIME) OVER (PARTITION BY M2.REPORT_DATE), 2)    AS HUDDLE_TIME
          , ROUND(AVG(M2.PROJECT_TIME) OVER (PARTITION BY M2.REPORT_DATE), 2)   AS PROJECT_TIME
          , ROUND(AVG(M2.NUMERATOR) OVER (PARTITION BY M2.REPORT_DATE), 2)      AS NUMERATOR
          , ROUND(AVG(M2.DENOMINATOR) OVER (PARTITION BY M2.REPORT_DATE), 2)    AS DENOMINATOR
          , ROUND(AVG(M2.ACTIVITY_COUNT) OVER (PARTITION BY M2.REPORT_DATE), 2) AS ACTIVITY_COUNT
          , ROUND(AVG(M2.ERROR_COUNT) OVER (PARTITION BY M2.REPORT_DATE), 2)    AS ERROR_COUNT
          , ROUND(AVG(M2.ZERO_TIME_ACTIVITIES)
                      OVER (PARTITION BY M2.REPORT_DATE), 2)                    AS ZERO_TIME_ACTIVITIES
          , CASE WHEN M2.REPORT_DATE >= DATE_TRUNC('d', DATEADD('WEEK', -6, CURRENT_TIMESTAMP :: TIMESTAMP_NTZ))
                      THEN 'Yes'
                      ELSE 'No'
            END                                                                 AS LAST_6_WEEKS
          , Previous_day(M2.REPORT_DATE, 'su')                                  AS WEEK_START
          , CAST('Team' AS VARCHAR2(50))                                        AS METRIC_LEVEL
     FROM M2)
                                                                 --
                                                                 --
   , m5  AS (SELECT *
             FROM M3
    UNION ALL (SELECT *
               FROM M4))
SELECT *
FROM m5
WHERE BADGE = '{badge}'
ORDER BY m5.METRIC_LEVEL, m5.BADGE, m5.REPORT_DATE DESC;