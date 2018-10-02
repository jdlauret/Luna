SELECT
<<<<<<< Updated upstream
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
>>>>>>> Buyout_PrepayCalc
    T.SERVICE_NAME,
    INITCAP(C.FULL_NAME),
    C.EMAIL,
    INITCAP(T.SERVICE_ADDRESS),
    INITCAP(T.SERVICE_CITY),
    T.SERVICE_STATE,
    T.SERVICE_ZIP_CODE
FROM VSLR.RPT.T_PROJECT AS T
INNER JOIN VSLR.RPT.T_CONTACT AS C ON C.CONTACT_ID = T.CONTRACT_SIGNER
<<<<<<< HEAD
=======
=======
>>>>>>> Stashed changes
    T.SERVICE_NUMBER,
    C.FULL_NAME,
    C.EMAIL,
    T.SERVICE_ADDRESS,
    T.SERVICE_CITY,
    T.SERVICE_STATE,
    T.SERVICE_ZIP_CODE
FROM VSLR.RPT.T_PROJECT AS T
INNER JOIN VSLR.RPT.T_CONTACT AS C ON C.CONTACT_ID =T.CONTRACT_SIGNER
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Buyout_PrepayCalc
=======
>>>>>>> Stashed changes
WHERE T.SERVICE_NUMBER = '{service_number}';

SELECT
    P.SERVICE_NUMBER,
<<<<<<< Updated upstream
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
>>>>>>> Buyout_PrepayCalc
    L.SYSTEM_SIZE_ACTUAL,
    P.REMAINING_CONTRACT_TERM
FROM VSLR.RPT.V_LOAN_DETAILS AS L
INNER JOIN VSLR.RPT.T_PROJECT AS P ON L.PROJECT_NAME = P.PROJECT_NAME
<<<<<<< HEAD
WHERE P.SERVICE_NUMBER = '{service_number}'
=======
=======
>>>>>>> Stashed changes
    C.SYSTEM_SIZE_ACTUAL_KW,
    P.REMAINING_CONTRACT_TERM
FROM VSLR.RPT.T_PROJECT AS P
INNER JOIN VSLR.RPT.T_CAD AS C ON P.PROJECT_ID = C.PROJECT_ID
WHERE P.SERVICE_NUMBER = '{service_number}'
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
WHERE P.SERVICE_NUMBER = '{service_number}'
>>>>>>> Buyout_PrepayCalc
=======
>>>>>>> Stashed changes
