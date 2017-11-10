class input_protection:
    def __init__(self, num_inputs=1, errs_per_input=3, errs_total=None):
        self.num_inputs = num_inputs
        self.errs_per_input = errs_per_input
        self.errs_total = errs_total

        self.err_map = {}
        self.err_count = 0

    def __call__(self, target_function):
        def wrapped(*args):
            input_queues = args[:self.num_inputs]
            output_queues = args[self.num_inputs:]

            inputs = tuple([q.get() for q in input_queues])
            pass_args = inputs + output_queues

            try:
                target_function(*pass_args)
            except Exception as err:

                if inputs not in self.err_map:
                    self.err_map[inputs] = []

                self.err_map[inputs].append(err)
                self.err_count += 1

                if len(self.err_map[inputs]) >= self.errs_per_input or \
                        (self.errs_total and self.err_count >= self.errs_total):
                    raise self.err_map[inputs][0]
                else:
                    for i, q in zip(inputs, input_queues):
                        q.put(i)

                    return

        return wrapped
