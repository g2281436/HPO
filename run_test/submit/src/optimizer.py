import numpy as np
from aiaccel.optimizer.abstract_optimizer import AbstractOptimizer


class MyOptimizer(AbstractOptimizer):
    """An optimizer class with a random algorithm.

    """
    def __init__(self, options: dict) -> None:
        super().__init__(options)

    def generate_parameter(self) -> None:
        """Generate parameters.

        Args:
            number (Optional[int]): A number of generating parameters.

        Returns:
            List[Dict[str, Union[str, float, List[float]]]]: A created
            list of parameters.
        """
        new_params = []
        hp_list = self.params.get_parameter_list()

        for hp in hp_list:
            value = np.random.normal(3, 0.1)
            value = min(max(value, hp.lower), hp.upper)
            new_param = {
                'parameter_name': hp.name,
                'type': hp.type,
                'value': value
            }
            new_params.append(new_param)
        
        return new_params
