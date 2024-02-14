class ReturnDirectException(Exception):
    """
      **Description:**

      A custom exception to detect the tasks which their return direct is active and force the \
      Task Executor to stop execution and directly return to user.
    """

    def __init__(self, message="Return direct."):
        self.message = message
        super().__init__(self.message)
