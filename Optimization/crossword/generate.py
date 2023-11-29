import sys
import itertools

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for structure, words in self.domains.items():
            to_remove = set()
            for word in words:
                if len(word) != structure.length:
                    to_remove.add(word)
            self.domains[structure] = self.domains[structure].difference(to_remove)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y]:
            i, j = self.crossword.overlaps[x, y]

            reference_letters = set()
            for word in self.domains[y]:
                reference_letters.add(word[j])

            to_remove = set()
            for word in self.domains[x]:
                if word[i] not in reference_letters:
                    to_remove.add(word)

            new_domain = self.domains[x].difference(to_remove)

            if new_domain != self.domains[x]:
                self.domains[x] = new_domain
                return True
            elif new_domain == self.domains[x]:
                return False
            
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = set()
            for variable in self.crossword.variables:
                to_add = set(itertools.product((variable,), self.crossword.neighbors(variable)))
                arcs.update(set(to_add))

        while arcs != set():
            current_pair = arcs.pop()
            x, y = current_pair
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                arcs.update((neighbor, x) for neighbor in self.crossword.neighbors(x) if neighbor != y)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)
            
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        uniqueness = list()
        for key, value in assignment.items():
            uniqueness.append(value)
            if key.length != len(value):
                return False

            for neighbor in self.crossword.neighbors(key):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[key, neighbor]
                    if assignment[key][i] != assignment[neighbor][j]:
                        return False

        return len(uniqueness) == len(set(uniqueness))

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_rank = dict()
        for word_1 in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    for word_2 in self.domains[neighbor]:
                        if word_1[i] != word_2[j]:
                            count += 1
                word_rank[word_1] = count

        sorted_word_strings_list = sorted(word_rank.keys(), key=lambda key: word_rank[key])

        return sorted_word_strings_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variable_rank = dict()
        degree_rank = dict()
        for variable, domain in self.domains.items():
            if variable not in assignment:
                variable_rank[variable] = len(domain)
                degree_rank[variable] = len(self.crossword.neighbors(variable))

        min_values_domain = [variable for variable, domain_size in variable_rank.items() if domain_size == min(variable_rank.values())]
        max_values_degree = [variable for variable, neighbors in degree_rank.items() if neighbors == max(degree_rank.values())]


        if len(min_values_domain) == 1:
            return min_values_domain[0]
        elif len(min_values_domain) > 1:
            return max_values_degree[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        variable = self.select_unassigned_variable(assignment)

        for word in self.order_domain_values(variable, assignment):
            assignment[variable] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            del assignment[variable]
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
