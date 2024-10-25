import itertools


class Sentence():
    """
    Clase base para representar una oración lógica.
    """

    def evaluate(self, model):
        """
        Evalúa la oración lógica utilizando un modelo.
        En este caso, es un método abstracto que será implementado en clases derivadas.
        """
        raise Exception("nada que evaluar")

    def formula(self):
        """
        Devuelve una representación de la fórmula lógica en forma de cadena de texto.
        """
        return ""

    def symbols(self):
        """
        Devuelve un conjunto de todos los símbolos presentes en la oración lógica.
        """
        return set()

    @classmethod
    def validate(cls, sentence):
        """
        Valida si un objeto es una instancia de la clase Sentence.
        """
        if not isinstance(sentence, Sentence):
            raise TypeError("debe ser una oración lógica")

    @classmethod
    def parenthesize(cls, s):
        """
        Coloca paréntesis en una expresión si no los tiene ya.
        """
        def balanced(s):
            """
            Verifica si una cadena tiene paréntesis balanceados.
            """
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):
    """
    Representa un símbolo lógico.
    """

    def _init_(self, name):
        self.name = name

    def _eq_(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def _hash_(self):
        return hash(("symbol", self.name))

    def _repr_(self):
        return self.name

    def evaluate(self, model):
        """
        Evalúa el valor del símbolo en un modelo dado.
        """
        try:
            return bool(model[self.name])
        except KeyError:
            raise EvaluationException(f"variable {self.name} no está en el modelo")

    def formula(self):
        return self.name

    def symbols(self):
        """
        Devuelve el conjunto que contiene solo este símbolo.
        """
        return {self.name}


class Not(Sentence):
    """
    Representa una negación lógica.
    """
    def _init_(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def _eq_(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def _hash_(self):
        return hash(("not", hash(self.operand)))

    def _repr_(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        """
        Evalúa la negación, invirtiendo el valor del operando.
        """
        return not self.operand.evaluate(model)

    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        return self.operand.symbols()


class And(Sentence):
    """
    Representa una conjunción lógica (Y).
    """
    def _init_(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def _eq_(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def _hash_(self):
        return hash(
            ("and", tuple(hash(conjunct) for conjunct in self.conjuncts))
        )

    def _repr_(self):
        conjunctions = ", ".join(
            [str(conjunct) for conjunct in self.conjuncts]
        )
        return f"And({conjunctions})"

    def add(self, conjunct):
        """
        Añade un nuevo conjunción a la lista.
        """
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        """
        Evalúa si todas las conjunciones son verdaderas.
        """
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        """
        Devuelve la fórmula de la conjunción.
        """
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula())
                           for conjunct in self.conjuncts])

    def symbols(self):
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    """
    Representa una disyunción lógica (O).
    """
    def _init_(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def _eq_(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def _hash_(self):
        return hash(
            ("or", tuple(hash(disjunct) for disjunct in self.disjuncts))
        )

    def _repr_(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        """
        Evalúa si al menos una de las disyunciones es verdadera.
        """
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        """
        Devuelve la fórmula de la disyunción.
        """
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join([Sentence.parenthesize(disjunct.formula())
                            for disjunct in self.disjuncts])

    def symbols(self):
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    """
    Representa una implicación lógica (si... entonces...).
    """
    def _init_(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def _eq_(self, other):
        return (isinstance(other, Implication)
                and self.antecedent == other.antecedent
                and self.consequent == other.consequent)

    def _hash_(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def _repr_(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        """
        Evalúa la implicación.
        """
        return ((not self.antecedent.evaluate(model))
                or self.consequent.evaluate(model))

    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    """
    Representa una bicondicional lógica (si y solo si).
    """
    def _init_(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def _eq_(self, other):
        return (isinstance(other, Biconditional)
                and self.left == other.left
                and self.right == other.right)

    def _hash_(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def _repr_(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        """
        Evalúa si ambas proposiciones tienen el mismo valor de verdad.
        """
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))

    def formula(self):
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """
    Verifica si la base de conocimiento implica una consulta.
    """

    def check_all(knowledge, query, symbols, model):
        """
        Verifica si la base de conocimiento implica la consulta en un modelo dado.
        """

        # Si el modelo tiene una asignación para cada símbolo
        if not symbols:

            # Si la base de conocimiento es verdadera en el modelo, entonces la consulta también debe ser verdadera
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        else:

            # Elige uno de los símbolos restantes no utilizados
            remaining = symbols.copy()
            p = remaining.pop()

            # Crea un modelo donde el símbolo es verdadero
            model_true = model.copy
            model_true[p] = True

            # Create a model where the symbol is false
            model_false = model.copy()
            model_false[p] = False

            # Ensure entailment holds in both models
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all symbols in both knowledge and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Check that knowledge entails query
    return check_all(knowledge, query, symbols, dict())
