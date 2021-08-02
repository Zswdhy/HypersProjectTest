import unittest


class MyTest(unittest.TestCase):
    def test_update(self):
        check_fields = ['id', 'e_job', 'province', 'city']
        print(check_fields)

        input_fields = ['asdada']

        self.assertEqual((set(input_fields) <= set(check_fields)), False)

        input_fields = ['id', 'e_job', 'province', 'city']
        self.assertEqual((set(input_fields) <= set(check_fields)), True)


if __name__ == '__main__':
    unittest.main()
