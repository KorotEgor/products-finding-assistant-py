INSERT INTO requests (request)
VALUES
    ('test_req1');

INSERT INTO products (request_id, name, url, price, avg_grade, num_of_grades)
VALUES
    (1, 'test_name', 'test_url', 1, 2.0, 3);
