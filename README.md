# FairSort 
<div>
    <a href="https://ieeexplore.ieee.org/abstract/document/10772283">
      <img alt="Static Badge" src="https://img.shields.io/badge/Journal-TKDE-green">
    </a>
    <a>
        <img alt="Static Badge" src="https://img.shields.io/badge/License-MIT-blue">
    </a>
</div>

Paper : [FairSort: Learning to Fair Rank for Personalized
Recommendations in Two-Sided Platforms.](https://arxiv.org/abs/2412.00424)
 Accepted by TKDE (Nov. 26, 2024)

Authors: Guoli Wu, Zhiyong Feng, Shizhan Chen, Hongyue Wu, Xiao Xue, Jianmao Xiao, Guodong Fan, Hongqi Chen, Jingyu Li


<div align=center><img src="FairSortDiagram.png" width="1300"/></div>

## Abstract
Traditional recommendation systems focus on maximizing user satisfaction by suggesting their favorite items. This user-centric approach may lead to unfair exposure distribution among the providers. On the contrary, a provider-centric design might become unfair to the users. Therefore, this paper proposes a re-ranking model FairSort to find a trade-off solution among user-side fairness, provider-side fairness, and personalized recommendations utility. Previous works habitually treat this issue as a knapsack problem, incorporating both-side fairness as constraints.
In this paper, we adopt a novel perspective, treating each recommendation list as a runway rather than a knapsack. In this perspective, each item on the runway gains a velocity and runs within a specific time, achieving re-ranking for both-side fairness. Meanwhile, we ensure the Minimum Utility Guarantee for personalized recommendations by designing a Binary Search approach. This can provide more reliable recommendations compared to the conventional greedy strategy based on the knapsack problem. We further broaden the applicability of FairSort, designing two versions for online and offline recommendation scenarios. Theoretical analysis and extensive experiments on real-world datasets indicate that FairSort can ensure more reliable personalized recommendations while considering fairness for both the provider and user.

## Hyperparameter setting


<img src="img_2.png" alt="图片描述" width="85%" height="auto">

[//]: # (![img_2.png]&#40;img_2.png&#41;)

[//]: # (![img_1.png]&#40;img_1.png&#41;)

## Run the code
After installation, you can clone this repository
```
"git lfs clone https://github.com/13543024276/FairSort.git" [or] "git clone git@github.com:13543024276/FairSort.git"
cd FairSort/FairSort_OffLine or cd FairSort/FairSort_OffLine
[such as Amazon]
python FairSort_Online_Amazon.py 
        
```


## DataSet

1-Ctrip Flight Dataset. The entire dataset contains data
from 3,814 customers, 6,006 kinds of air tickets, and 25,190
orders. It also provides basic information on customers, air
ticket class, air ticket price, flight time, airline company of
the ticket, and other information. we adopt the state-of-the-
art collaborative filtering air ticket recommendation algorithm
to process the data and obtain a preference matrix.

2-Amazon Review Dataset. We used data from, which
has the largest data due to its large number of reviews. We
pre-filtered items and users with less than 10 reviews or being
reviewed and only consider reviews of items in the “Clothing
Shoes and Jewelry” category, which has the largest number
of reviews. And using the well-known matrix decomposition
model to estimate users’ preference scores for items,
the dataset does not provide information between items and
providers. We then model the providers by clustering methods,
with 1-100 items clustered into one category. The processed
dataset contains 1,851 users, 7,538 items, 161 providers.

3-Google Local DataSet. This dataset is unique, where each
item represents an individual provider. This was released in
and contains reviews about local businesses from Google
Maps. It also filtered items and users who participated in
reviews less than 10 times, then obtained a dataset containing
3,335 users, 4,927 items (providers), and 97,658 reviews. The
data is processed by using an implicit decomposition algorithm
based on location information.
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Citation
```
@article{wu2024fairsort,
  title={FairSort: Learning to Fair Rank for Personalized Recommendations in Two-Sided Platforms},
  author={Wu, Guoli and Feng, Zhiyong and Chen, Shizhan and Wu, Hongyue and Xue, Xiao and Xiao, Jianmao and Fan, Guodong and Chen, Hongqi and Li, Jingyu},
  journal={IEEE Transactions on Knowledge and Data Engineering},
  year={2024},
  publisher={IEEE}
}
```


