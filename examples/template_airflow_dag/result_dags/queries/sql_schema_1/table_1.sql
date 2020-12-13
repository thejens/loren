CREATE TABLE table_1
  AS (
        SELECT some_field AS a
        FROM some_table
        WHERE date == "{{ ds }}"
  )

