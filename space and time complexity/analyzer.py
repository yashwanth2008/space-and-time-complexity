from tree_sitter import Language, Parser
import tree_sitter_cpp as tscpp


class ComplexityAnalyzer:

    def __init__(self, source_code):

        self.source_code = source_code

        self.language = Language(tscpp.language())
        self.parser = Parser(self.language)

        self.tree = self.parser.parse(
            source_code.encode("utf-8")
        )

    def analyze(self):

        print("\n-------analysing wait broo-------\n")

        result = self.analyze_node(self.tree.root_node)

        print("\n-------finally the result is-------\n")

        if result:
            print(
                "i think the complexity(Keep in mind i am not sure either):",
                result
            )
        else:
            print("Complexity: O(1)")
    def analyze_function_call(self, node):

        function_name = None

        for child in node.children:

            if child.type == "identifier":
                function_name = self.get_text(child)
                break

        if function_name:
            print("\nFound function call:", function_name)

        return None

    def analyze_node(self, node):

        if node.type == "function_definition":

            print("There is a function")

            results = []

            for child in node.children:

                result = self.analyze_node(child)

                if result:
                    results.append(result)

            return self.combine_sequential(results)

        if node.type == "for_statement":
            return self.analyze_for_loop(node)

        if node.type == "while_statement":
            return self.analyze_while_loop(node)

        if node.type == "if_statement":
            return self.analyze_if_statement(node)
        if node.type == "call_expression":
            return self.analyze_function_call(node)

        results = []

        for child in node.children:

            result = self.analyze_node(child)

            if result:
                results.append(result)

        return self.combine_sequential(results)

    def analyze_while_loop(self, node):

        print("\nThere is a while-loop")

        condition = None
        body = None

        for child in node.children:

            if child.type == "parenthesized_expression":
                condition = self.get_text(child)

            elif child.type == "compound_statement":
                body = child

        if condition:
            print("Condition:", condition)
        else:
            print("it was not ther")

        if body:

            body_text = self.get_text(body)

            if "/=" in body_text or "*=" in body_text:

                print("Detected logarithmic reduction")
                print("Loop complexity: O(log n)")

                return "O(log n)"

            elif "++" in body_text or "--" in body_text:

                print("Detected linear growth")
                print("Loop complexity: O(n)")

                return "O(n)"

        print("Unknown while-loop complexity")

        return "O(?)"

    def analyze_for_loop(self, node):

        print("\nThere is a for-loop")

        loop_complexity = self.get_loop_complexity(node)

        print("Loop complexity:", loop_complexity)

        body = None

        for child in node.children:

            if child.type == "compound_statement":
                body = child

        if body:

            nested_loop_complexity = self.find_nested_loop(body)

            if nested_loop_complexity:

                print(
                    "Nested complexity:",
                    nested_loop_complexity
                )

                return self.multiply_complexity(
                    loop_complexity,
                    nested_loop_complexity
                )

        return loop_complexity

    def find_nested_loop(self, node):

        for child in node.children:

            if child.type == "for_statement":

                return self.analyze_for_loop(child)

            if child.type == "while_statement":

                return self.analyze_while_loop(child)

            result = self.find_nested_loop(child)

            if result:

                return result

        return None

    def analyze_if_statement(self, node):

        print("\nFound if-statement")

        condition = None
        has_else = False

        for child in node.children:

            if child.type == "parenthesized_expression":

                condition = self.get_text(child)

            elif child.type == "else_clause":

                has_else = True

        if condition:

            print("Condition:", condition)

        if has_else:

            print("Found else-branch")

        print("If/else complexity: O(1)")

        return "O(1)"

    def get_loop_complexity(self, node):

        update = None

        for child in node.children:

            if child.type in [
                "update_expression",
                "assignment_expression"
            ]:

                update = self.get_text(child)

        if update:

            print("Update:", update)

            if "*=" in update or "/=" in update:

                print("Type: Logarithmic")

                return "O(log n)"

            elif "++" in update or "--" in update:

                print("Type: Linear")

                return "O(n)"

        return "O(?)"

    def multiply_complexity(self, outer, inner):

        if outer == "O(n)" and inner == "O(n)":

            return "O(n²)"

        if outer == "O(n)" and inner == "O(log n)":

            return "O(n log n)"

        if outer == "O(log n)" and inner == "O(n)":

            return "O(n log n)"

        if outer == "O(log n)" and inner == "O(log n)":

            return "O((log n)²)"

        return f"{outer} × {inner}"


    def combine_sequential(self, complexities):

        if not complexities:

            return None

        if len(complexities) == 1:

            return complexities[0]

        return max(
            complexities,
            key=self.complexity_rank
        )


    def complexity_rank(self, complexity):

        if complexity == "O(1)":

            return 1

        if complexity == "O(log n)":

            return 2

        if complexity == "O(n)":

            return 3

        if complexity == "O(n log n)":

            return 4

        if complexity == "O(n²)":

            return 5

        if complexity == "O(n³)":

            return 6

        return 0

    def get_text(self, node):

        return self.source_code[
            node.start_byte:node.end_byte
        ]
def analyze_file(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        source_code = file.read()

    analyzer = ComplexityAnalyzer(source_code)

    analyzer.analyze()
