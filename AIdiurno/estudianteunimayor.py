from logic import *

lluvia = Symbol("lluvia")
BBC = Symbol("BBC")
unimayor = Symbol("unimayor")

knowledge = And(
    Implication(Not(lluvia), BBC),
    Or(BBC, unimayor),
    Not(And(BBC, unimayor)),
    unimayor
)

print(model_check(knowledge, lluvia))
