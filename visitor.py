from parsimonious.nodes import NodeVisitor

class IniVisitor(NodeVisitor):
    def visit_expr(self, node, visited_children):
        """ Returns the overall output. """
        output = []
        for child in visited_children[0]:
            output.append(child)
        return output
    
    def visit_term(self, node, visited_children):
        return visited_children[0]

    def visit_factor(self, node, visited_children):
        return visited_children[0]
    
    def visit_const(self, node, visited_children):
        return node.text
    
    def visit_add(self, node, visited_children):
        return node.text
    
    def visit_mul(self, node, visited_children):
        return node.text

    def visit_left(self, node, visited_children):
        return node.text
    
    def visit_right(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node

class BackwardVisitor():
    def visit(self,node,ctx):
        node.accept(self,ctx)

    def calc_grad(self,node,ctx):
        op = ctx['op']
        prev_grad = ctx['grad']
        co_value = ctx['value']

        if op == '+':
            node.grad += prev_grad
            return prev_grad
        else:
            node.grad += prev_grad*co_value
            return prev_grad*co_value

    def visit_Expression(self,node,ctx):
        grad = self.calc_grad(node,ctx)
        ctx_lhs = {'grad':grad,'op':node.op,'value':node.rhs.value}
        ctx_rhs = {'grad':grad,'op':node.op,'value':node.lhs.value}
        if node.op == '*':
            node.lhs_grad = node.rhs.value
            node.rhs_grad = node.lhs.value
        else:
            node.lhs_grad = 1
            node.rhs_grad = 1

        self.visit(node.lhs,ctx_lhs)
        self.visit(node.rhs,ctx_rhs)
    
    def visit_Variable(self,node,ctx):
        self.calc_grad(node,ctx)