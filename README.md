# Week 7: Codex CLI Hands-On

## Analytical Question

How do home sale prices differ between neighborhoods in Ames, Iowa?

## Codex Session Date

October 18, 2026

## Dataset

This analysis uses the AmesHousing dataset 

## Analytical Approach

The analysis compares home sale prices across neighborhoods and uses median sale price as the comparison measure. Additional statistics include mean sale price, number of sales, minimum, maximum, and first and third quartiles. All 28 neighborhoods are included in the summary table, while the visualization is limited to neighborhoods with at least 20 recorded sales. All observations, including outliers, were retained.

## Key Findings

The analysis found large differences in sale prices across the neighborhoods. StoneBr had the highest median sale price at 319,000 while MeadowV had the lowest at 88,250. Across the entire dataset, the median sale price was 160,000 and the mean was approximately 180,796. These findings suggest that home sale prices vary substantially by neighborhood.

## Repository Contents

- `AmesHousing-1.csv` - Original dataset
- `analysis/neighborhood_analysis.py` - Python analysis script
- `analysis/neighborhood_summary.csv` - Summary statistics
- `analysis/median_sale_price_by_neighborhood.svg` - Visualization of median sale prices
- `analysis/neighborhood_findings.md` - Summary of findings and limitations
- `prompts/` - Full Codex prompt history
- `log/ai-workflow-log.md` - AI Workflow Log
- `reflection.md` - Reflection

## Reproducing the Analysis

Run the following

`python analysis/neighborhood_analysis.py`
