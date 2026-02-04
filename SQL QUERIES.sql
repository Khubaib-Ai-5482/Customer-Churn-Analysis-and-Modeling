use new_schema;


SELECT 
    ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate
FROM
    churn_modelling;


SELECT 
    Exited, COUNT(*)
FROM
    churn_modelling
GROUP BY Exited;


SELECT 
    Geography,
    ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate
FROM
    churn_modelling
GROUP BY Geography;


SELECT 
    Gender,
    ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate
FROM
    churn_modelling
GROUP BY Gender;


SELECT 
    CASE
        WHEN Age BETWEEN 18 AND 30 THEN '18-30'
        WHEN Age BETWEEN 31 AND 45 THEN '31-45'
        WHEN Age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END AS age_group,
    ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate
FROM
    churn_modelling
GROUP BY age_group;


SELECT 
    Exited, AVG(Age)
FROM
    churn_modelling
GROUP BY Exited;


SELECT 
    CASE
        WHEN CreditScore < 580 THEN 'Poor'
        WHEN CreditScore BETWEEN 580 AND 669 THEN 'Fair'
        WHEN CreditScore BETWEEN 670 AND 739 THEN 'Good'
        ELSE 'Excellent'
    END AS credit_group,
    ROUND(SUM(Exited) * 100.0 / COUNT(*), 2) AS churn_rate
FROM
    churn_modelling
GROUP BY credit_group;