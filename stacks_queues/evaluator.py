from stacks import ArrayStack, LinkedListStack

class Evaluator():
    '''
    a Dijkstra implementation to evaluate a fully parenthesized
    numeric expression and return the resulting number
    for integers between 0 and 9
    '''
    
    def __init__(self):
        self.ARITHMETIC_OPERATORS = ['+', '-', '*']
        self.operators_stack = ArrayStack()
        self.operands_stack  = ArrayStack()
        
    def evaluate(self, expression):
        expression = expression.replace(' ', '')
        
        for token in expression:
            if token in self.ARITHMETIC_OPERATORS:
                self.operators_stack.push(token)
            
            elif token == ')':
                operator = self.operators_stack.pop()
                operand1 = self.operands_stack.pop()
                operand2 = self.operands_stack.pop()
                
                if operator == '+':
                    self.operands_stack.push(operand1+operand2)
                elif operator == '-':
                    self.operands_stack.push(operand2-operand1)
                elif operator == '*':
                    self.operands_stack.push(operand1*operand2)
                    
            elif token != '(':
                self.operands_stack.push(int(token))
                
        return self.operands_stack.pop()
    
    
class EvaluatorLinkedList(Evaluator):
    def __init__(self):
        self.ARITHMETIC_OPERATORS = ['+', '-', '*']
        self.operators_stack = LinkedListStack()
        self.operands_stack  = LinkedListStack()