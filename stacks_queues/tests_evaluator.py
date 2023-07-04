import unittest
from evaluator import Evaluator, EvaluatorLinkedList

class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator()

    def test_evaluate_single_expression(self):
        # Test evaluating a single expression
        expression = "(3+4)"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 7)

        expression = "(5-2)"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 3)

        expression = "(2*6)"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 12)

    def test_evaluate_nested_expression(self):
        # Test evaluating a nested expression
        expression = "((3+2)*4)"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 20)

        expression = "((5-2)*(2+3))"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 15)

        expression = "((8+2)*(6-1))"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 50)

    def test_evaluate_complex_expression(self):
        # Test evaluating a complex expression
        expression = "(((4*3)-2)+((5+2)*3))"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 31)

        expression = "((((8-1)*2)+6)-(3-2))"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 19)

        expression = "((7-3)*(2+(8-4)))"
        result = self.evaluator.evaluate(expression)
        self.assertEqual(result, 24)

class EvaluatorLinkedListTest(EvaluatorTest):
    def setUp(self):
        self.evaluator = EvaluatorLinkedList()

if __name__ == '__main__':
    unittest.main()
