INSERT INTO requests (request)
VALUES
    ('test_req1'),
    ('test_req2');

INSERT INTO products (request_id, name, url, price, avg_grade, num_of_grades)
VALUES
    (1, 'test_name1', 'test_url1', 1, 2.0, 3),
    (2, 'test_name2', 'test_url2', 1, 2.0, 3);
