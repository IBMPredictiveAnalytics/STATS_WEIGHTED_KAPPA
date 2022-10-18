# STATS_WEIGHTED_KAPPA
## Weighted kappa statistic using linear or quadratic weights
Provides the weighted version of Cohen's kappa for two raters, using either linear or quadratic weights, as well as confidence interval and test statistic.

**NOTE This functionality is now implemented natively, and can be found in the menus at Analyze->Scale->Weighted Kappa**.

---
Requirements
----
- IBM SPSS Statistics 19 or later and the corresponding IBM SPSS Statistics-Integration Plug-in for Python.

---
Installation intructions
----
1. Open IBM SPSS Statistics
2. Navigate to Utilities -> Extension Bundles -> Download and Install Extension Bundles
3. Search for the name of the extension and click Ok. Your extension will be available.

---
Tutorial
----
See STATS_WEIGHTED_KAPPA_DIALOG_HELP.htm and STATS_WEIGHTED_KAPPA_SYNTAX_HELP.htm in documentation

### Installation Location

Analyze →

&nbsp;&nbsp;Scale →

&nbsp;&nbsp;&nbsp;&nbsp;Weighted Kappa 

### UI
<img width="616" alt="image" src="https://user-images.githubusercontent.com/19230800/196474174-6884372c-1ace-4298-ad36-f38c1da6ef1b.png">

### Syntax
Example:

STATS WEIGHTED KAPPA VARIABLES=salary salbegin
 /OPTIONS WTTYPE=1 CILEVEL=95.

---
License
----

- Apache 2.0
                              
Contributors
----

  - JKP, IBM SPSS
