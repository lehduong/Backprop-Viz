from abc import ABC
import numpy as np
from NameCreator import NameCreator

class Tensor(ABC):
    def calculation(self):
        #Compute the value of current node
        pass

    def accept(self,visitor,ctx):
        visitor.visit(self,ctx)

class Expression(Tensor):
    def __init__(self,lhs:Tensor,op:str,rhs:Tensor,name=None):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.value = self.calculation()
        self.grad = 0
        #self.name = NameCreator.getName() if name is None else name
        self.name = name if name else str(self.value)
        self.lhs_grad = 0 
        self.rhs_grad = 0
        
    def calculation(self):
        if self.op == '+':
            return self.lhs.calculation() + self.rhs.calculation()
        else:
            return self.lhs.calculation() * self.rhs.calculation()

    def accept(self,visitor,ctx):
        visitor.visit_Expression(self,ctx)

    def __str__(self,level=0):
        return self.get_str()

    def get_str(self,level=0):
        return '\n'+'\t'*level+"<var: "+self.name+ " grad:"+str(self.grad)+" value:"+str(self.value)+">"+\
                self.lhs.get_str(level+1)+\
                '\n'+'\t'*(level+1)+ '<'+str(self.op)+'/>'+\
                self.rhs.get_str(level+1)+\
                '\n'+'\t'*level+"</>"
    
class Variable(Tensor):
    def __init__(self,name:str,value:float=0):
        self.name = name
        self.value = value
        self.grad = 0
        
    def calculation(self):
        return self.value
    
    def accept(self,visitor,ctx):
        visitor.visit_Variable(self,ctx)
    
    def get_str(self,level=0):
        return '\n'+'\t'*level+"<"+'var:'+ self.name + " value:"+str(self.value)+ ' grad:' +str(self.grad)+"/>"
    
    def __str__(self,level=0):
        return self.get_str()

#[['d', '*', ['(', ['h', '+', [['(', ['g', '+', ['k', '*', ['(', ['j', '+', ['a']], ')']]], ')'], '*', 'i']], ')']], '+', ['a', '*', 'x']]
def create_binary_tree(output,lookup):
    """
    :param output: output of visitor
    :param lookup: dictionary map name -> Variable object
    """
    if type(output) is str:
        if output in lookup:
            instance = lookup[output]
            if not isinstance(instance,Expression):
                return instance
            return Expression(create_binary_tree(instance.lhs.name,lookup),
                        instance.op,
                        create_binary_tree(instance.rhs.name,lookup),output)
        else:
            tmp = Variable(output)
            lookup[output] = tmp
            return tmp

    # 
    if len(output) == 1:
        if output[0] in lookup:
            instance = lookup[output[0]]
            if not isinstance(instance,Expression):
                return instance
            return Expression(create_binary_tree(instance.lhs.name,lookup),
                        instance.op,
                        create_binary_tree(instance.rhs.name,lookup),output[0])
        else:
            tmp = Variable(output[0])
            lookup[output[0]] = tmp
            return tmp
    else:
        # parenthesis => calculate the expression inside it
        if output[0] == '(':
            return create_binary_tree(output[1],lookup)
        # recursive construct tree
        return Expression(create_binary_tree(output[0],lookup),
                        output[1],
                        create_binary_tree(output[2],lookup))