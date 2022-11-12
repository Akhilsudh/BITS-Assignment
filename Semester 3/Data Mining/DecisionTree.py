import numpy as np
class CustomDecisionTree:
    def __init__(self, max_depth=-1):
        # Custom tree
        self.custom_tree = {}
        # Column labels: These are used only to print the tree.
        self.column_names = []
        self.max_depth = max_depth
   
    class Question:
        def __init__(self, column, value):
            self.column = column
            self.value = value

        def match(self, example):
            # Compare the feature value in an example to the
            # feature value in this question.
            val = example[self.column]
            #check if feature value is numeric or not
            if (isinstance(val, int) or isinstance(val, float)):
                return val >= self.value
            else:
                return val == self.value

        def get(self, custom_obj):
            # This is just a helper method to print
            # the question in a readable format.
            condition = "=="
            #check if feature value is numeric or not
            if (isinstance(self.value, int) or isinstance(self.value, float)):
                condition = ">="
            return "Is %s %s %s?" % (
                custom_obj.column_names[self.column], condition, str(self.value))
    
    class Decision_Node:
        def __init__(self,
                     question,
                     true_branch,
                     false_branch,
                     gain,
                     sample_size,
                     class_map):
            self.question = question
            self.true_branch = true_branch
            self.false_branch = false_branch
            self.sample_size = sample_size
            self.gain = gain
            self.class_map = class_map
    
    #Counts the number of each type of example in a dataset.
    def class_counts(self, rows):
        counts = {}  # a dictionary of label -> count.
        for row in rows:
            # in our dataset format, the label is always the last column
            label = row[-1]
            if label not in counts:
                counts[label] = 0
            counts[label] += 1
        return counts

    class Leaf:
        def __init__(self, rows, custom_obj):
            self.predictions = custom_obj.class_counts(rows)
        
    #Find the unique values for a column in a dataset.
    def unique_vals(self, rows, col):
        return set([row[col] for row in rows])

    #Partitions a dataset. For each row in the dataset, check if it matches the question. If so, add it to 'true rows', 
    #otherwise, add it to 'false rows'.
    def partition(self, rows, question):
        true_rows, false_rows = [], []
        for row in rows:
            if question.match(row):
                true_rows.append(row)
            else:
                false_rows.append(row)
        return true_rows, false_rows

    #Calculate the Gini Impurity for a list of rows.
    def gini(self, rows):
        counts = self.class_counts(rows)
        impurity = 1
        for lbl in counts:
            prob_of_lbl = counts[lbl] / float(len(rows))
            impurity -= prob_of_lbl**2
        return impurity

    #Information Gain : The uncertainty of the starting node, minus the weighted impurity of two child nodes.
    def info_gain(self, left, right, current_uncertainty):
        p = float(len(left)) / (len(left) + len(right))
        return current_uncertainty - p * self.gini(left) - (1 - p) * self.gini(right)

    #Find the best question to ask by iterating over every feature / value and calculating the information gain.
    def find_best_split(self, rows):
        best_gain = 0  # keep track of the best information gain
        best_question = None  # keep train of the feature / value that produced it
        current_uncertainty = self.gini(rows)
        n_features = len(rows[0]) - 1  # number of columns

        for col in range(n_features):  # for each feature

            values = set([row[col] for row in rows])  # unique values in the column

            for val in values:  # for each value

                question = self.Question(col, val)

                # try splitting the dataset
                true_rows, false_rows = self.partition(rows, question)

                # Skip this split if it doesn't divide the dataset.
                if len(true_rows) == 0 or len(false_rows) == 0:
                    continue

                # Calculate the information gain from this split
                gain = self.info_gain(true_rows, false_rows, current_uncertainty)

                # Keep track of best gain
                if gain >= best_gain:
                    best_gain, best_question = gain, question

        return best_gain, best_question

    def build_tree(self, rows, level=0):
        # base case: Max depth reached
        if((self.max_depth != -1) and (level > self.max_depth)):
            return self.Leaf(rows, self)
        
        # Try partitioing the dataset on each of the unique attribute,
        # calculate the information gain,
        # and return the question that produces the highest gain.
        gain, question = self.find_best_split(rows)

        # Base case: no further info gain
        # Since we can ask no further questions,
        # we'll return a leaf.
        if gain == 0:
            return self.Leaf(rows, self)

        # If we reach here, we have found a useful feature / value
        # to partition on.
        true_rows, false_rows = self.partition(rows, question)

        level = level + 1
        # Recursively build the true branch.
        true_branch = self.build_tree(true_rows, level)

        # Recursively build the false branch.
        false_branch = self.build_tree(false_rows, level)

        # Return a Question node.
        # This records the best feature / value to ask at this point,
        # as well as the branches to follow
        # dependingo on the answer.
        return self.Decision_Node(question, true_branch, false_branch, gain, len(rows), self.class_counts(rows))
    
    def classify(self, row, node):
        # Base case: we've reached a leaf
        if isinstance(node, self.Leaf):
            no_stroke = 0
            has_stroke = 0
            if(node.predictions.get(0) != None):
                no_stroke = node.predictions.get(0)
            if(node.predictions.get(1) != None):
                has_stroke = node.predictions.get(1)
            if(no_stroke > has_stroke):
                return 0
            else:
                return 1
            
        # Decide whether to follow the true-branch or the false-branch.
        # Compare the feature / value stored in the node to the example we're considering.
        if node.question.match(row):
            return self.classify(row, node.true_branch)
        else:
            return self.classify(row, node.false_branch)

    def build(self, training_data):
        #convert dataframe to numpy
        training_data_array = np.squeeze(np.asarray(training_data))
        self.column_names = training_data.columns
        #build decision tree
        self.custom_tree = self.build_tree(training_data_array)
    
    def print_custom_tree(self, node, depth = 5, spacing="",level=0):
        if((depth != -1) and (level > depth)):
            return
        # Base case: we've reached a leaf
        if isinstance(node, self.Leaf):
            print (spacing + "value = ", node.predictions)
            return
        level = level + 1;
        # Print the question at this node
        print (spacing + str(node.question.get(self)))
        print (spacing + "Gain = " + str(node.gain))
        print (spacing + "samples = " + str(node.sample_size))
        print (spacing + "value = " + str(node.class_map))

        # Call this function recursively on the true branch
        print (spacing + '--> True:')
        self.print_custom_tree(node.true_branch, depth, spacing + "  ", level)

        # Call this function recursively on the false branch
        print (spacing + '--> False:')
        self.print_custom_tree(node.false_branch, depth, spacing + "  ", level)
    
    def print_tree(self, depth = -1):
        self.print_custom_tree(self.custom_tree, depth, "", 0)
        
    def predict(self, test_data):
        #Convert dataframe to numpy arrays
        test_data_array = np.squeeze(np.asarray(test_data))
        predicted_output = [];
        for row in test_data_array:
            #classify current row in test array using custom decision tree
            predicted_output.append(self.classify(row, self.custom_tree))
        return (predicted_output)