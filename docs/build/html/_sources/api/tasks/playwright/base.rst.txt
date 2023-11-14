Playwright
==========




This code defines a base class named BaseBrowser that inherits from BaseTask. 
This class is intended for tasks related to browser interactions using the Playwright library. 
The code uses conditional imports to handle situations where the Playwright library is not available.



    .. py:function:: validate_environment(cls, values: Dict)

        Validate that 'playwright' package exists in the environment.

        :param cls: The class itself.
        :type: cls: type
        :param values: The dictionary containing the values for validation.
        :type values: Dict
        :return: The original values.
        :rtype: Dict
        :rise ImportError: If the 'playwright' package is not installed.



