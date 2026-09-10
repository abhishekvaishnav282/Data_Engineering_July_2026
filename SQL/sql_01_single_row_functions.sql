-- ================================================================
-- Oracle SQL Single-Row Functions - HR.EMPLOYEES Examples Only
-- Database: Oracle
-- ================================================================


-- ============================
-- CHARACTER FUNCTIONS
-- ============================

-- 1. UPPER()
select first_name,
       upper(first_name)
  from hr.employees;


-- 2. LOWER()
select first_name,
       lower(first_name)
  from hr.employees;


-- 3. INITCAP()
select first_name,
       initcap(first_name)
  from hr.employees;


-- 4. LENGTH()
select first_name,
       length(first_name)
  from hr.employees;


-- 5. SUBSTR()
select first_name,
       substr(
          first_name,
          1,
          3
       )
  from hr.employees;


-- 6. CONCAT()
select first_name,
       last_name,
       concat(
          first_name,
          last_name
       )
  from hr.employees;


-- 7. REPLACE()
select first_name,
       replace(
          first_name,
          'a',
          '@'
       )
  from hr.employees;


-- 8. TRIM()
select first_name,
       trim(first_name)
  from hr.employees;


-- 9. LTRIM()
select first_name,
       ltrim(first_name)
  from hr.employees;


-- 10. RTRIM()
select first_name,
       rtrim(first_name)
  from hr.employees;


-- 11. LPAD()
select employee_id,
       lpad(
          employee_id,
          6,
          '0'
       ) as formatted_employee_id
  from hr.employees;


-- 12. RPAD()
select first_name,
       rpad(
          first_name,
          15,
          '.'
       )
  from hr.employees;


-- 13. ASCII()
select first_name,
       ascii(first_name)
  from hr.employees;




-- ============================
-- NUMERIC FUNCTIONS
-- ============================

-- 15. CEIL()
select salary,
       salary / 12,
       ceil(salary / 12)
  from hr.employees;


-- 16. FLOOR()
select salary,
       salary / 12,
       floor(salary / 12)
  from hr.employees;


-- 17. MOD() - Even Employee IDs
select employee_id,
       first_name
  from hr.employees
 where mod(
   employee_id,
   2
) = 0;


-- 18. ABS()
select employee_id,
       salary,
       abs(salary - 10000) as salary_difference
  from hr.employees;


-- 19. POWER()
select employee_id,
       salary,
       power(
          salary,
          2
       )
  from hr.employees;


-- 20. SQRT()
select employee_id,
       salary,
       sqrt(salary)
  from hr.employees;