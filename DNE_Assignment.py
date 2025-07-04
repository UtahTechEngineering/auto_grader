class Assignment:
    def __init__(self, title, id, input_shapes, output_shapes, input_ranges, input_labels, output_labels, function_to_evaluate, class_to_evaluate=None, class_inputs=None, max_score=100.0):
        self.title = title
        self.id = id
        self.input_shapes = input_shapes
        self.output_shapes = output_shapes
        self.input_ranges = input_ranges
        self.input_labels = input_labels
        self.output_labels = output_labels
        self.function_to_evaluate = function_to_evaluate
        self.class_to_evaluate = class_to_evaluate
        self.class_inputs = class_inputs
        self.max_score = max_score