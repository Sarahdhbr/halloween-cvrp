# Sources

## Main references

1. James Fitzpatrick, Deepak Ajwani, Paula Carroll. *A scalable learning approach for the capacitated vehicle routing problem*. Computers & Operations Research 171, 106787 (2024). https://doi.org/10.1016/j.cor.2024.106787
2. Wouter Kool, Herke van Hoof, Max Welling. *Attention, Learn to Solve Routing Problems!* ICLR 2019. https://arxiv.org/abs/1803.08475
3. Yeong-Dae Kwon, Jinho Choo, Byoungjip Kim, Iljoo Yoon, Youngjune Gwon, Seungjai Min. *POMO: Policy Optimization with Multiple Optima for Reinforcement Learning*. NeurIPS 2020. https://arxiv.org/abs/2010.16011
4. Éric D. Taillard, Stefan Voß. *POPMUSIC: Partial Optimization Metaheuristic under Special Intensification Conditions*. In *Essays and Surveys in Metaheuristics*, pp. 613-629. Kluwer (2002). https://doi.org/10.1007/978-1-4615-1507-4_27
5. Paulo Roberto de Oliveira da Costa, Stefano Mauceri, Paula Carroll, Fabiano Pallonetto. *A Genetic Algorithm for a Green Vehicle Routing Problem*. Electronic Notes in Discrete Mathematics 64, 65-74 (2018). https://doi.org/10.1016/j.endm.2018.01.008
6. G. Clarke, J. W. Wright. *Scheduling of Vehicles from a Central Depot to a Number of Delivery Points*. Operations Research 12(4), 568-581 (1964). https://doi.org/10.1287/opre.12.4.568
7. S. Erdoğan, E. Miller-Hooks. *A green vehicle routing problem*. Transportation Research Part E 48(1), 100-114 (2012). https://doi.org/10.1016/j.tre.2011.08.001

References 6 and 7 are cited through the main paper; their full texts were not consulted.

## Solver

Saved exact solutions were computed with HiGHS through `scipy.optimize.milp`. See the logs in `data/`.

## Data

Coordinates, demands and resource parameters form a fixed teaching instance (seed 2196). They are not benchmark data from the papers.

## Character images

The images in `assets/portraits/` are small thumbnails found through Google Images, used to decorate a student presentation. Their original source and licence are unknown. The characters and images belong to their respective rights holders and are not covered by any licence for this repository. This project has no affiliation with them, and any image will be removed on request.
