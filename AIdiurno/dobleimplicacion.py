# Function to display truth table for double implication
def double_implication(p, q):
    return (p and q) or (not p and not q)

# Generate the truth table
def truth_table():
    print(" P     Q     P ↔ Q ")
    print("---------------------")
    for p in [True, False]:
        for q in [True, False]:
            result = double_implication(p, q)
            print(f"{p}|\t{q}|\t{result}")

# Call the function to display the truth table
truth_table()
