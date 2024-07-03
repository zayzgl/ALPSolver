# ALPSolver: A Solver for Assumable Logic Programming


## Abstract
Assumable Logic Programming (ALP), an extension of Answer Set Programming (ASP), has been theoretically demonstrated to possess significant advantages in addressing problems involving incomplete information. Therefore, the development of an ALP solver is urgently needed to facilitate further research and applications. This paper proposes a solving algorithm named Answer Set Based View Search (ASBVS) and its optimizations to compute the results of ALP programs. Based on this, the `ALPSolver` has been implemented and integrated into an online platform for public use. This paper experimentally validates the correctness of the solving algorithm and confirms the advantages of ALP in handling default information, indirect exception and abductive reasoning. Additionally, the experimental results demonstrate the effectiveness of the optimization algorithm, with a notable increase in effectiveness as the problem scale increases.

## Introduction

Assumable Logic Programming (ALP) has been theoretically proven to possess notable advantages in addressing problems involving incomplete information. However, the experimental validation and application of ALP have been somewhat impeded due to the lack of solvers. The main contributions of this paper are listed as follows: 

(1) This paper proposes an ALP solving algorithm and refines it through optimization. Based on the syntax and semantics of ALP, we propose a solving algorithm called Answer Set Based View Search (ASBVS) that computes the stable model to ALP programs, consisting of three steps: assumption set establishment, mode selection, and belief set establishment. In order to enhance the solving efficiency of this algorithm, we utilize ALP program preprocessing and enumeration pruning to reduce the search space, thereby proposing the optimized ASBVS, referred to as OASBVS. 

(2) This paper implements an ALP solver and develops an online system for the deep research and application of ALP. To validate the correctness and feasibility of ASBVS and OASBVS, we implemented the `ALPSolver` based on them. Additionally, we developed an online ALP system to facilitate the theoretical and practical advancements in ALP. 

(3) To validate the correctness of ALP theoretical advancements and the effectiveness of OASBVS, this paper conducts experiments from three perspectives, including comparative experiments between ASP, GPT-4 and ALP, abductive reasoning of ALP and program scale impact on optimization. The in-depth experiments and analysis fill the gaps in ALP research.

***


## Experiments

In this section, experimental results from three aspects that includes comparative experiment, abductive reasoning and the program scale impact on optimization are thoroughly introdueced.


### Comparative Experiment

To compare the ability of ASP, GPT-4 and ALP in handling default information and indirect exception, we conducted experiments where all systems were tasked with solving the same problems. Additionally, the results obtained were compared with manually computed results to verify the correctness of the ALP solving algorithm.

**(1) Default information processing**

For **Example 1 (Bird Flight Problem)**, the following are the results from ASP, GPT-4 and ALP.

- **ASP**

  Example 1 can be transform into the following ASP rules: 

  ````
  fly :- bird, not -fly.
  wing :- fly.
  bird.
  -wing.
  ````

  The ASP solving process was halted prematurely due to the emergence of a contradiction, where both `wing` and `-wing` were inferred simultaneously.

- **GPT-4**

  The response of example 1 for GPT-4 is 

  ````
  Let's analyze the given statements and the relationships between them:
  	1.If an organism is a bird and there is no evidence to suggest its incapacity for flight, it is generally inferred that the organism is capable of flight.
  	2.If a bird is capable of flight, it is necessarily equipped with wings.
  	3.There is a bird (New Zealand kiwi) without any wing (the wings have degenerated to invisibility).
  Given this information, we can draw the following conclusions:
  	1.The kiwi is a bird.
  	2.The kiwi lacks visible wings (the wings have degenerated to invisibility).
  Based on statement 2, a bird that is capable of flight must have wings. The kiwi, however, lacks visible wings. Therefore, we can infer that: The kiwi is not capable of flight.
  Thus, the final conclusion is: The kiwi, despite being a bird, is not capable of flight because it lacks wings.
  ````

  This conclusion is erroneous, as the used rule is a general rule that should be overridden in the presence of specific circumstances. In fact, when a bird without wings is encountered, it is inconclusive to determine its flight capability.

- **ALP**

  The ALP program of Example 1 is

  ````
  fly :- bird : fly.
  wing :- fly.
  bird.
  -wing.
  ````

  The outcome of `ALPSolver` is

  ````
  VIEWS={<{bird,-wing},{bird,-wing}>}
  ````

  This result is correct, indicating that no further conclusions can be inferred based on the given assumptions `{bird,-wing}`. ALP always reduces default information based on the assumptions prior to computing a final result, which prevents the emergence of unreasonable outcomes.

For **Example 2 (Athlete Problem)**, below are the respective responses from ASP, GPT-4 and ALP.

- **ASP**

  Example 2 can be transform into the following ASP rules:

  ````
  marathon :- available, not -marathon.
  relay :- available, not -relay.
  :- marathon, relay.
  available.
  ````

  The result of ASP is none because there is no answer set satisfying the conditions by the semantics of ASP. This underscores the limitations of ASP in handling default information.

- **GPT-4**

  The response of example 2 for GPT-4 is

  ````
  When arranging competition events, the athlete should give priority to choosing marathons. If the athlete unable to participate in the marathon, he can choose to participate in the relay. Under no circumstances can the athlete participate in both marathon and relay races simultaneously.
  ````

  It is obvious that GPT-4 introduces the preferences into the athlete's decision without cause, which is called hallucination. When the relay is presented as the primary option during inquiry, GPT-4 exhibits a preference for selecting the relay race on the contrary.

- **ALP**

  The ALP program of Example 2 is

  ````
  marathon :- available: marathon.
  relay :- available: relay.
  :- marathon, relay.
  available.
  ````

  The outcome of `ALPSolver` is

  ````
  VIEWS={<{marathon,available},{marathon,available}>,<{relay,available},{relay,available}>}
  ````

  This means that if the athlete is available to participate in marathon, then choose marathon. Similarly, the same principle applies to the relay race. However, the athlete will not concurrently participate in both the marathon and the relay race. This correct result demonstrates the strong capability of ALP in handling default information.



In conclusion, as shown in the following table, when processing default information, ALP has considerable advantages over ASP and GPT-4, as its reasoning is both accurate and stable. Additionally, the experimental results also validate the correctness and effectiveness of the ALP solving algorithm that is the foundation of the `ALPSolver`.

|       Program       |                 Correct Result                  |      ASP      |         GPT-4         |                       ALP                       |
| :-----------------: | :---------------------------------------------: | :-----------: | :-------------------: | :---------------------------------------------: |
| Bird Flight Problem |                  {bird, -wing}                  | unsatisfiable |  {bird, -wing, -fly}  |                  {bird, -wing}                  |
|   Athlete Problem   | {marathon, avaliable},<br /> {relay, avaliable} | unsatisfiable | {marathon, avaliable} | {marathon, avaliable},<br /> {relay, avaliable} |



**(2) Indirect Exception Inference**

According to example 1, for the statement that in the absence of evidence to the contrary a bird is presumed to be capable of flight, the corresponding ASP rule is `fly :- bird, not -fly.`, while the ALP rule is `fly :- bird: fly.`. 

For ASP, the solving process of Clingo was interrupted because the inference of `wing` conflicted with `-wing` already present in the program. However, this situation is not a problem with the program itself but rather an error in Clingo’s processing of rules containing default information. The rule should be applied when it does not result in a contradiction. In the case of `{bird, -wing}`, this rule should not be used, which is the key reason why the ASP solver fails to solve example 1.

In contrast, ALP can effectively address indirect exception. Based on the assumption `{bird, -wing}`, ALP will prohibit the use of the rule by reduction, avoiding the occurrence of conflicts. Hence, ALP demonstrates superior capacity for indirect exception inference compared to ASP.


## Abductive Reasoning

Abductive reasoning is the process of inferring the most reasonable explanations of certain results, in other words, it employs inference to identify the causes behind the results. We validated that ALP possesses the capability of abductive reasoning as ABLP93 by the following experiments.

For **Conclusion 1** in the paper, the results of Example 3 are shown in the following table.

|                                            | Result |
| :----------------------------------------: | :----: |
| The abductive minimal belief set of ABLP93 |  {p}   |
|        The min_RC belief set of ALP        |  {p}   |

For **Conclusion 2** in the paper, the abductive results of a positive observation G = p are shown in the following table.

|        | Result |
| :----: | :----: |
| ABLP93 |   ∅    |
|  ALP   |   ∅    |

To sum up, the empirical evidence demonstrates that ALP possesses the capability of abductive reasoning as ABLP93, which serves as a complement to theoretical evidence.


## Evaluation

To evaluate the performance of the ALP solving algorithm ASBVS and its optimization OASBVS, experiments were conducted from two distinct perspectives.

The tested programs of different scales are as follows, where `n` denotes the number of unit atoms, for example, as the Bird Flight Problem, `n` is the number of birds and a unit includes 4 atoms; while as the Athlete Problem, `n` is the number of athletes and a unit includes 3 atoms.

<table>
    <tr>
        <td align='center'rowspan ='2'><b>Program</b></td>
        <td align='center' colspan='2'><b>ASBVS</b></td>
        <td align='center'colspan='2'><b>OASBVS</b></td>
    </tr>
    <tr>
        <td align='center'>Number of Atoms</td>
        <td align='center'>Number of Possible Assumption Sets</td>
        <td align='center'>Number of Atoms</td>
        <td align='center'>Number of Possible Assumption Sets</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=1)</td>
        <td align='center'>4</td>
        <td align='center'>2<sup>4</sup></td>
        <td align='center'>3</td>
        <td align='center'>2<sup>2</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=2)</td>
        <td align='center'>8</td>
        <td align='center'>2<sup>8</sup></td>
        <td align='center'>6</td>
        <td align='center'>2<sup>4</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=3)</td>
        <td align='center'>12</td>
        <td align='center'>2<sup>12</sup></td>
        <td align='center'>9</td>
        <td align='center'>2<sup>6</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=4)</td>
        <td align='center'>16</td>
        <td align='center'>2<sup>16</sup></td>
        <td align='center'>12</td>
        <td align='center'>2<sup>8</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=5)</td>
        <td align='center'>20</td>
        <td align='center'>2<sup>20</sup></td>
        <td align='center'>15</td>
        <td align='center'>2<sup>10</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=6)</td>
        <td align='center'>24</td>
        <td align='center'>2<sup>24</sup></td>
        <td align='center'>18</td>
        <td align='center'>2<sup>12</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=7)</td>
        <td align='center'>28</td>
        <td align='center'>2<sup>28</sup></td>
        <td align='center'>21</td>
        <td align='center'>2<sup>14</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=8)</td>
        <td align='center'>32</td>
        <td align='center'>2<sup>32</sup></td>
        <td align='center'>24</td>
        <td align='center'>2<sup>16</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=9)</td>
        <td align='center'>36</td>
        <td align='center'>2<sup>36</sup></td>
        <td align='center'>27</td>
        <td align='center'>2<sup>18</sup></td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=10)</td>
        <td align='center'>40</td>
        <td align='center'>2<sup>40</sup></td>
        <td align='center'>30</td>
        <td align='center'>2<sup>20</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=1)</td>
        <td align='center'>3</td>
        <td align='center'>2<sup>3</sup></td>
        <td align='center'>3</td>
        <td align='center'>2<sup>2</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=2)</td>
        <td align='center'>6</td>
        <td align='center'>2<sup>6</sup></td>
        <td align='center'>6</td>
        <td align='center'>2<sup>4</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=3)</td>
        <td align='center'>9</td>
        <td align='center'>2<sup>9</sup></td>
        <td align='center'>9</td>
        <td align='center'>2<sup>6</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=4)</td>
        <td align='center'>12</td>
        <td align='center'>2<sup>12</sup></td>
        <td align='center'>12</td>
        <td align='center'>2<sup>8</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=5)</td>
        <td align='center'>15</td>
        <td align='center'>2<sup>15</sup></td>
        <td align='center'>15</td>
        <td align='center'>2<sup>10</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=6)</td>
        <td align='center'>18</td>
        <td align='center'>2<sup>18</sup></td>
        <td align='center'>18</td>
        <td align='center'>2<sup>12</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=7)</td>
        <td align='center'>21</td>
        <td align='center'>2<sup>21</sup></td>
        <td align='center'>21</td>
        <td align='center'>2<sup>14</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=8)</td>
        <td align='center'>24</td>
        <td align='center'>2<sup>24</sup></td>
        <td align='center'>24</td>
        <td align='center'>2<sup>16</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=9)</td>
        <td align='center'>27</td>
        <td align='center'>2<sup>27</sup></td>
        <td align='center'>27</td>
        <td align='center'>2<sup>18</sup></td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=10)</td>
        <td align='center'>30</td>
        <td align='center'>2<sup>30</sup></td>
        <td align='center'>30</td>
        <td align='center'>2<sup>20</sup></td>
    </tr>
</table>

<table>
    <tr>
    </tr>
</table>
**(1) Efficiency**

The below table illustrates the impact of different optimization combinations on algorithm efficiency, where the unit of time in the table is ms.

|         Program          |  ASBVS  | Preprossing | Prunning | OASBVS |
| :----------------------: | :-----: | :---------: | :------: | :----: |
| Bird Flight Problem(n=1) |  0.009  |    0.009    |  0.007   | 0.007  |
| Bird Flight Problem(n=2) |  0.029  |    0.025    |  0.015   | 0.012  |
| Bird Flight Problem(n=3) |  0.195  |    0.173    |  0.051   | 0.038  |
| Bird Flight Problem(n=4) |  2.107  |    1.085    |  0.130   | 0.103  |
| Bird Flight Problem(n=5) | 14.363  |    4.262    |  0.487   | 0.401  |
| Bird Flight Problem(n=6) | 115.206 |   17.749    |  1.970   | 1.755  |
| Bird Flight Problem(n=7) | 993.831 |   97.828    |  8.233   | 6.926  |
|   Athlete Problem(n=1)   |  0.010  |    0.011    |  0.009   | 0.009  |
|   Athlete Problem(n=2)   |  0.024  |    0.022    |  0.017   | 0.013  |
|   Athlete Problem(n=3)   |  0.153  |    0.131    |  0.043   | 0.039  |
|   Athlete Problem(n=4)   |  1.244  |    0.761    |          | 0.108  |
|   Athlete Problem(n=5)   | 10.953  |    5.203    |          | 0.434  |
|   Athlete Problem(n=6)   | 99.573  |   22.088    |          | 1.805  |
|   Athlete Problem(n=7)   | 905.978 |   127.549   |  8.705   | 7.364  |

In terms of algorithm efficiency, OASBVS has the highest speedup ratio that increases significantly with the scale of ALP program. In addition, the enumeration pruning enhances the algorithm more effectively than preprocessing; however, their combination yields the optimal result.

**(2) Program Scale Impact on Optimization**

The metrics that includes solving time (ms) and speedup ratio of different programs are presented in the following table.

<table>
    <tr>
        <td align='center'rowspan ='2'><b>Program</b></td>
        <td align='center'><b>ASBVS</b></td>
        <td align='center'colspan='2'><b>OASBVS</b></td>
    </tr>
    <tr>
        <td align='center'>Time</td>
        <td align='center'>Time</td>
        <td align='center'>Speedup Ratio</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=1)</td>
        <td align='center'>0.009</td>
        <td align='center'>0.007</td>
        <td align='center'>1.285</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=2)</td>
        <td align='center'>0.029</td>
        <td align='center'>0.012</td>
        <td align='center'>2.417</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=3)</td>
        <td align='center'>0.195</td>
        <td align='center'>0.038</td>
        <td align='center'>5.131</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=4)</td>
        <td align='center'>2.107</td>
        <td align='center'>0.103</td>
        <td align='center'>20.456</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=5)</td>
        <td align='center'>14.363</td>
        <td align='center'>0.401</td>
        <td align='center'>35.818</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=6)</td>
        <td align='center'>115.206</td>
        <td align='center'>1.755</td>
        <td align='center'>65.644</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=7)</td>
        <td align='center'>993.831</td>
        <td align='center'>6.926</td>
        <td align='center'>143.493</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=8)</td>
        <td align='center'>timeout</td>
        <td align='center'>31.366</td>
        <td align='center'>--</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=9)</td>
        <td align='center'>timeout</td>
        <td align='center'>125.104</td>
        <td align='center'>--</td>
    </tr>
    <tr>
        <td align='center'>Bird Flight Problem(n=10)</td>
        <td align='center'>timeout</td>
        <td align='center'>597.417</td>
        <td align='center'>--</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=1)</td>
        <td align='center'>0.101</td>
        <td align='center'>0.009</td>
        <td align='center'>1.111</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=2)</td>
        <td align='center'>0.024</td>
        <td align='center'>0.013</td>
        <td align='center'>1.846</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=3)</td>
        <td align='center'>0.153</td>
        <td align='center'>0.039</td>
        <td align='center'>3.923</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=4)</td>
        <td align='center'>1.244</td>
        <td align='center'>0.108</td>
        <td align='center'>11.518</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=5)</td>
        <td align='center'>10.953</td>
        <td align='center'>0.434</td>
        <td align='center'>25.237</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=6)</td>
        <td align='center'>99.573</td>
        <td align='center'>1.805</td>
        <td align='center'>55.165</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=7)</td>
        <td align='center'>905.978</td>
        <td align='center'>7.364</td>
        <td align='center'>123.028</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=8)</td>
        <td align='center'>timeout</td>
        <td align='center'>35.291</td>
        <td align='center'>--</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=9)</td>
        <td align='center'>timeout</td>
        <td align='center'>148.454</td>
        <td align='center'>--</td>
    </tr>
    <tr>
        <td align='center'>Athlete Problem(n=10)</td>
        <td align='center'>timeout</td>
        <td align='center'>623.507</td>
        <td align='center'>--</td>
    </tr>
</table>

It is noteworthy that as the problem scale increases, the speedup ratio of OASBVS rapidly improves, which indicates that the effectiveness of the optimization algorithm becomes increasingly advantageous with larger problem scales.


## Conclusion

Assumable Logic Programming (ALP) has been theoretically proven to possess notable advantages in addressing problems involving incomplete information [6]. However, the experimental validation and application of ALP have been somewhat impeded due to the lack of solvers. This paper proposes a solving algorithm called Answer Set Based View Search (ASBVS) to compute the results of ALP program based on its syntax and semantics. To enhance algorithm efficiency, this paper further proposes two optimization methods, forming Optimized ASBVS (OASBVS). The `ALPSolver` has been implemented and embedded into an online platform for further research. This paper experimentally validates the correctness of the solving algorithm and confirms the advantages of ALP in handling default information, indirect exception and abductive reasoning. The experimental results also demonstrate the effectiveness of the optimization algorithm, with a significant increase in effectiveness as the problem scale increases. However, OASBVS focuses solely on optimizing the establishment of assumption sets, with potential for further improvement from other aspects. Moreover, a ALP solver capable of solving ALP programs containing variables is under development.
