-- ================================================================
-- Day 8 Assignment
-- Schema: hr.employees, hr.departments
-- ================================================================


-- ============================
-- SELF-PRACTICE
-- ============================

-- SP1. Using a self-join, show two levels of hierarchy:
-- employee -> manager -> manager's manager (if exists).
select e.first_name as emp_first,
       e.last_name as emp_last,
       m.first_name as mgr_first,
       m.last_name as mgr_last,
       m2.first_name as mgr_mgr_first,
       m2.last_name as mgr_mgr_last
  from hr.employees e
  left join hr.employees m
on e.manager_id = m.employee_id
  left join hr.employees m2
on m.manager_id = m2.employee_id;


-- SP2. List departments that have no employees
-- (use RIGHT JOIN or a subquery / NOT EXISTS from departments).
select d.department_id,
       d.department_name
  from hr.departments d
 where not exists (
   select 1
     from hr.employees e
    where e.department_id = d.department_id
);


-- ============================
-- MEDIUM 
-- ============================

-- M1. List all employees (employee_id, first_name, last_name) and department_name;
-- include employees with no department (LEFT JOIN).
select e.employee_id,
       e.first_name,
       e.last_name,
       d.department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;


-- M2. For each employee show first_name, last_name, and manager's first_name and last_name (self-join).
select e.first_name,
       e.last_name,
       m.first_name as manager_first_name,
       m.last_name as manager_last_name
  from hr.employees e
  left join hr.employees m
on e.manager_id = m.employee_id;


-- M3. List all departments (department_id, department_name) and count of employees;
-- include departments with 0 employees.
select d.department_id,
       d.department_name,
       count(e.employee_id) as employee_count
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 group by d.department_id,
          d.department_name;


-- M4. Show employees who have no department
-- (LEFT JOIN to departments, WHERE d.department_id IS NULL).
select e.employee_id,
       e.first_name,
       e.last_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id
 where d.department_id is null;


-- M5. List employee first_name, last_name, and department_name;
-- use COALESCE(d.department_name, 'No Dept').
select e.first_name,
       e.last_name,
       coalesce(
          d.department_name,
          'No Dept'
       ) as department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;


-- M6. Show all departments and total salary in each (include departments with 0 salary).
select d.department_id,
       d.department_name,
       sum(e.salary) as total_salary
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 group by d.department_id,
          d.department_name;


-- M7. For each employee show name and manager name;
-- use LEFT JOIN so employees without manager appear.
select e.first_name,
       e.last_name,
       m.first_name as manager_first_name,
       m.last_name as manager_last_name
  from hr.employees e
  left join hr.employees m
on e.manager_id = m.employee_id;


-- M8. List departments (department_name) that have no employees
-- (RIGHT JOIN from employees to departments then WHERE e.employee_id IS NULL, or NOT EXISTS).
select d.department_name
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 where e.employee_id is null;


-- M9. Show employee_id, first_name, department_id, department_name;
-- include employees with null department_id.
select e.employee_id,
       e.first_name,
       e.department_id,
       d.department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;


-- M10. List all departments and the number of employees;
-- show 0 for departments with no employees.
select d.department_id,
       d.department_name,
       count(e.employee_id) as employee_count
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 group by d.department_id,
          d.department_name;


-- M11. Show employee name and manager name;
-- alias manager columns as mgr_first_name, mgr_last_name.
select e.first_name,
       e.last_name,
       m.first_name as mgr_first_name,
       m.last_name as mgr_last_name
  from hr.employees e
  left join hr.employees m
on e.manager_id = m.employee_id;


-- M12. List employees (first_name, last_name) and department_name;
-- include employees whose department_id is not in hr.departments (LEFT JOIN, they get NULL).
select e.first_name,
       e.last_name,
       d.department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;


-- M13. Show department_id, department_name, and employee count;
-- include departments with 0 employees.
select d.department_id,
       d.department_name,
       count(e.employee_id) as employee_count
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 group by d.department_id,
          d.department_name;


-- M14. For each employee show employee_id, salary, department_name;
-- use NVL(d.department_name, 'Unassigned').
select e.employee_id,
       e.salary,
       nvl(
          d.department_name,
          'Unassigned'
       ) as department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;


-- M15. List employees with their manager's employee_id and manager's last_name (self-join).
select e.employee_id,
       e.first_name,
       e.last_name,
       m.employee_id as mgr_employee_id,
       m.last_name as mgr_last_name
  from hr.employees e
  left join hr.employees m
on e.manager_id = m.employee_id;


-- M16. Show all departments (department_name) and min salary in that department
-- (NULL for no employees).
select d.department_id,
       d.department_name,
       min(e.salary) as min_salary
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 group by d.department_id,
          d.department_name;


-- M17. List employees who have a manager (manager_id IS NOT NULL)
-- and show manager's first_name.
select e.employee_id,
       e.first_name,
       e.last_name,
       m.first_name as manager_first_name
  from hr.employees e
  join hr.employees m
on e.manager_id = m.employee_id
 where e.manager_id is not null;


-- M18. Show employee_id, first_name, department_name;
-- include employees with no department (LEFT JOIN).
select e.employee_id,
       e.first_name,
       d.department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;


-- M19. List departments (department_id, department_name) and average salary;
-- include departments with no employees (avg NULL or 0).
select d.department_id,
       d.department_name,
       avg(e.salary) as avg_salary
  from hr.departments d
  left join hr.employees e
on d.department_id = e.department_id
 group by d.department_id,
          d.department_name;


-- M20. For each employee show name and department_name; if no department show 'N/A'.
select e.first_name,
       e.last_name,
       coalesce(
          d.department_name,
          'N/A'
       ) as department_name
  from hr.employees e
  left join hr.departments d
on e.department_id = d.department_id;