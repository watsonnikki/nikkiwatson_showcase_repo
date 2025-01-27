
# Optimal Sequencing of Biologic Treatment Progression in Crohn’s Disease
## Overview
This project explores the optimal sequencing of biologic therapies for managing Crohn's Disease using computational simulations in Python. The study assesses how different treatment sequences affect patient outcomes and explores the financial and disease burden implications.

## Author
Nikki Watson
Master’s student in Industrial and Operations Engineering and Data Science
University of Michigan

# Background
Crohn's Disease (CD) is a chronic autoimmune disorder without a known cure, requiring lifelong management. This project specifically investigates how the sequencing of biologic treatments impacts treatment efficacy and patient outcomes, considering the formation of anti-drug antibodies (ADAbs).

# Objective
To evaluate how treatment sequencing affects the failure rates of various biologics and to analyze the associated disease burden and costs.

# Methodology

**Simulation Model:** Used a 25-year linear compartmental model to simulate CD progression.
**Treatment Sequences:** Examined 50 sequences including TNF blockers, IL-12, IL-23 blockers, and JAK inhibitors.
**Outcome Variables:** Evaluated failure rates, disability-adjusted life years (DALYs), and treatment costs.

# Key Findings
1. Sequencing biologics starting with TNF blockers and ending with IL-12 and IL-23 blockers (Skyrizi) results in the best patient outcomes.
2. Sequences ending with JAK inhibitors were notably less effective.
3. High treatment costs during active phases overshadow costs associated with surgical intervention.

# Conclusion
Optimal sequencing can significantly affect Crohn's Disease management, potentially reducing disease burden and costs. The findings suggest further research into the order and interaction of biologic therapies.

# Implications
Healthcare providers can utilize insights from this model to reevaluate treatment protocols and potentially enhance patient care by selecting more effective treatment sequences.

# Limitations and Future Work

**Limitations:** Fixed failure rates assume static conditions, and individual variance in treatment efficacy is not accounted for.
**Future Research:** More extensive modeling including diverse treatment permutations and individual patient experiences is recommended.

# How to Use This Repository

**Code Structure:** The simulation model is implemented in Python and includes scripts for running the simulations and analyzing results.
**Data Sources:** Refer to the appendices for a list of biologics and their associated failure rates used in the model.

# Contact
For further information, contact Nikki Watson at nikkiwat@umich.edu.

