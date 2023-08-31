SELECT department_name,
    c.name,
    aid,
    pub.name,
    model,
    is_fixed,
    purchase_date,
    username
FROM (
        (
            public_assert pub
            JOIN category c on pub.cid = c.cid
        )
        JOIN user on pub.admin_id = user.user_id
    ) pub
    JOIN department d ON pub.department_id = d.department_id;
SELECT department_name,
    c.name,
    aid,
    pa.name,
    model,
    is_fixed,
    purchase_date,
    personal_id,
    username
FROM (
        (
            personal_assert pa
            JOIN category c on pa.cid = c.cid
        )
        JOIN user on pa.admin_id = user.user_id
    ) pa
    JOIN department d ON pa.department_id = d.department_id;
SELECT *
FROM personal_assert
WHERE personal_id = 104900;