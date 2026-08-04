-- Day 9 Assignment 
-- Schema: hr.employees, hr.departments



-- ============================
-- SELF-PRACTICE
-- ============================

-- SP1. Show average salary per job_id only for job_ids that have more than 5 employees.
select job_id,
       avg(salary) as avg_salary
  from hr.employees
 group by job_id
having count(*) > 5;


-- SP2. Show the sum of salary for department_id 50 only (one row).
select sum(salary) as total_salary
  from hr.employees
 where department_id = 50;


-- SP3. Show the maximum commission_pct per department_id (NULLs are ignored by MAX).
select department_id,
       max(commission_pct) as max_commission_pct
  from hr.employees
 group by department_id;


-- ============================
-- MEDIUM 
-- ============================

-- M1. Show total salary (SUM(salary)) for the whole company from hr.employees.
select sum(salary) as total_salary
  from hr.employees;


-- M2. Count employees per job_id.
select job_id,
       count(*) as employee_count
  from hr.employees
 group by job_id;


-- M3. Show average salary per department_id.
select department_id,
       avg(salary) as avg_salary
  from hr.employees
 group by department_id;


-- M4. List department_id and min(salary), max(salary) per department.
select department_id,
       min(salary) as min_salary,
       max(salary) as max_salary
  from hr.employees
 group by department_id;


-- M5. Count employees per department_id.
select department_id,
       count(*) as employee_count
  from hr.employees
 group by department_id;


-- M6. Show job_id and total salary per job.
select job_id,
       sum(salary) as total_salary
  from hr.employees
 group by job_id;


-- M7. List department_id and number of employees with non-null commission_pct.
select department_id,
       count(commission_pct) as commission_count
  from hr.employees
 group by department_id;


-- M8. Show min(hire_date) and max(hire_date) per job_id.
select job_id,
       min(hire_date) as earliest_hire,
       max(hire_date) as latest_hire
  from hr.employees
 group by job_id;


-- M9. Count total employees (COUNT(*)) in hr.employees.
select count(*) as total_employees
  from hr.employees;


-- M10. Show department_id, avg(salary), and count(*) per department.
select department_id,
       avg(salary) as avg_salary,
       count(*) as employee_count
  from hr.employees
 group by department_id;


-- M11. List job_id and average salary per job; order by average salary desc.
select job_id,
       avg(salary) as avg_salary
  from hr.employees
 group by job_id
 order by avg(salary) desc;


-- M12. Show department_id and sum(salary) for department_id in (50, 60, 80).
select department_id,
       sum(salary) as total_salary
  from hr.employees
 where department_id in ( 50,
                          60,
                          80 )
 group by department_id;


-- M13. Count employees per manager_id (include only where manager_id is not null).
select manager_id,
       count(*) as report_count
  from hr.employees
 where manager_id is not null
 group by manager_id;


-- M14. Show job_id and min(salary) per job.
select job_id,
       min(salary) as min_salary
  from hr.employees
 group by job_id;


-- M15. List department_id and max(hire_date) per department.
select department_id,
       max(hire_date) as latest_hire
  from hr.employees
 group by department_id;


-- M16. Show total salary for department_id 90 only.
select sum(salary) as total_salary
  from hr.employees
 where department_id = 90;


-- M17. Count distinct job_id values (COUNT(DISTINCT job_id)).
select count(distinct job_id) as distinct_job_count
  from hr.employees;


-- M18. Show department_id, job_id, and count(*) per (department_id, job_id).
select department_id,
       job_id,
       count(*) as employee_count
  from hr.employees
 group by department_id,
          job_id;


-- M19. List department_id and avg(salary) rounded to 2 decimals per department.
select department_id,
       round(
          avg(salary),
          2
       ) as avg_salary
  from hr.employees
 group by department_id;


-- M20. Show job_id and count of employees; only job_ids with at least 2 employees.
select job_id,
       count(*) as employee_count
  from hr.employees
 group by job_id
having count(*) >= 2;