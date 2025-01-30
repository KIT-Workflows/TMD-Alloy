# TMD-Alloy
Transition Metal Dicalcogenite, Alloys, Density functional theory, GQCA

# Colab

- Colab notebook for data visualization .

This notebook is used to compute the thermodynamic properties and statistical attributes from the ab initio calculations executed from the TMD-Alloy Workflow. Below, we describe the functions covered by the actual version.

```python
def root_lagrange_multiplier(x, T):
   """
Parameters:
        x (float): The composition of alloy, such as 0<=x<=1.
        T (float): Temperature in Kelvin.
Returns:
        eta (float): The value of Lagrange multiplier.
    """'
```

This function calculate the value of Lagrange multiplier η, which is related to the average composition constrain evaluated as x at temperature T.

```python
def xj(self, j, T, eta):
 """
    Calculates the Cluster probabilities for each class in GQCA.

    Parameters:
        j (int): number of class, in the same order of the input file gqca_inputs.yml.
        T (float): Temperature in Kelvin.
        eta (float): The value of Lagrange multiplier within GQCA.
    Returns:
        xj (float): The value of cluster probability for the j-th class of alloy.
    """
```

