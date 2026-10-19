# AI Workflow Log

## Prompt 1: Initial Data Exploration and Planning

**Date/Time:** October 18, 2026, 9:19 PM

**Prompt Objective:** Inspect the AmesHousing dataset, identify data quality issues, and recommend an analytical approach before proceeding with the full analysis.

**Codex Output:** Codex reported 2,930 observations, 82 variables, and 28 neighborhoods. It identified SalePrice and Neighborhood as the primary variables and examined missing values, sample sizes, sale conditions, and outliers. It recommended comparing neighborhood sale prices using medians, means, counts, and distribution summaries. 

**Accepted:** I agree with using the median sale price for the comparison because extreme sale prices could skew the average. I also agree with reporting additional summary statistics and sample sizes to provide context for the comparisons.

**Modified:** I decided to make the main visualization focus on neighborhoods with at least 20 sales but keep all neighborhoods in the summary table. 

**Rejected:** I did not support automatically removing unusually high or low sale prices without further investigation because they may represent legitimate transactions.

**Verification:** I reviewed the neighborhood counts and confirmed that they sum to 2,930. I also noticed an inconsistency in the missing-value summary: Codex reported 510 blank cells overall, but two individual columns alone accounted for 649 missing entries

**Next Steps:** The initial exploration helped clarify the analytical approach. The next prompt will address the missing-value discrepancy and provide more detailed instructions for the analysis.


## Prompt 2: Neighborhood Sale Price Analysis

**Date/Time:** October 18, 2026, approximately 10:36 PM

**Prompt Objective:** Explain the missing-value inconsistency identified from first response and generate a python analysis comparing sale prices across the neighborhoods

**Codex Output:** Codex corrected the missing-value total from 510 to 719 and separately identified 13278 "NA" values. It created a Python analysis script, a CSV containing summary statistics for all 28 neighborhoods, an SVG of a bar chart showing the 24 neighborhoods with at least 20 sales, and a findings summary. The script ran successfully and codex reported that the median sale prices ranged from $88,250 in MeadowV to $319,000 in StoneBr

**Accepted:** I accepted to use the median sale price as the primary comparison and including additional statistics for context. I also accepted the approach of including all neighborhoods in the summary table while limiting the visualization to those with at least 20 sales.

**Modified:** Codex corrected its earlier missing-value summary. It also revised its script to include more detailed missing-value counts

**Rejected:** No outputs were rejected

**Verification:** The generated files were reviewed. The 28 neighborhood counts sum to 2,930 observations and the 24 neighborhoods shown in the chart are correct. The chart labels and median prices are consistent with what is in the CSV. The summary stats in the CSV are consistent with calculations I preformed on the original dataset

**Next Steps:** The next step is to improve the chart visual and identify any other improvements before finalizing the analysis.


## Prompt 3: Visualization Improvements

**Date/Time:** October 18, 2026, 11:08 PM

**Prompt Objective:** Improve the appearance of the visualization

**Codex Output:** Codex updated the Python script and regenerated the chart SVG. The new chart has no vertical gridlines, a centered title, and neighborhoods ordered from highest to lowest.

**Accepted:** I accepted the revised visualization because it is cleaner and easier to read

**Modified:** I requested four specific changes based on my review of the initial chart

**Rejected:** No outputs were rejected

**Verification:** The revised chart was reviewed. Its labels, median prices, and sample sizes were compared with the summary CSV and were consistent

**Next Steps:** The next steps are verification and finishing the README and reflection.




