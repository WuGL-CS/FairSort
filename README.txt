Directory structure description：
├── README.txt                        // help
├── TFROM_quality_weighted.py                    // Code for TFROM on Ctrip datasets in offline scenario for Quality Weighted Fairness.
├── TFROM_quality_weighted_dynamic.py    // Code for TFROM on Ctrip datasets in online scenario for Quality Weighted Fairness.
├── TFROM_quality_weighted_dynamic_g&a.py    // Code for TFROM on Google and Amazon datasets in online scenario for Quality Weighted Fairness.
├── TFROM_quality_weighted_g&a.py                    // Code for TFROM on Google and Amazon datasets in offline scenario for Quality Weighted Fairness.
├── TFROM_uniform.py                    // Code for TFROM on Ctrip datasets in offline scenario for Uniform Fairness.
├── TFROM_uniform_dynamic.py    // Code for TFROM on Ctrip datasets in online scenario for Uniform Fairness.
├── TFROM_uniform_dynamic_g&a.py    // Code for TFROM on Google and Amazon datasets in online scenario for Uniform Fairness.
├── TFROM_uniform_g&a.py                    // Code for TFROM on Google and Amazon datasets in offline scenario for Uniform Fairness.
└──datasets                           // datasets
│   ├── data_amazon               // Amazon dataset
│        ├── Clothing_Shoes_and_Jewelry_5_2004.json.gz   // The original data of the Amazon dataset.
│        ├── preference_score.csv                 // Relevant rating matrix of the Amazon dataset.
│        ├── item_provider.csv                     // Correspondence table for items and providers of the Amazon dataset.
│   ├── data_ctrip               // Ctrip dataset
│        ├── Clothing_Shoes_and_Jewelry_5_2004.json.gz   // The original data of the Ctrip dataset.
│        ├── score_international.csv                 // Relevant rating matrix of the Ctrip dataset.
│        ├── ticket_international.csv                     // Correspondence table for items and providers of the Ctrip dataset.
│   ├── data_google              // Google dataset      
│        ├── CA_5.json.gz                          // Statistics of the Google dataset.
│        ├── preference_score.csv                 // Relevant rating matrix of the Google dataset.
│        └── item_provider.csv                     // Correspondence table for items and providers of the Google dataset.