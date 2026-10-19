# Neighborhood sale price findings

Source: `AmesHousing-1.csv` (2,930 sales, 82 variables). All valid sale records are retained.

Across all neighborhoods, the median sale price is $160,000.00; the mean is $180,796.06. Neighborhood medians range from $88,250.00 in MeadowV (n=37) to $319,000.00 in StoneBr (n=51).

## Neighborhood patterns

The complete summary table reports the number of sales, median, mean, minimum, first quartile, third quartile, and maximum for all 28 neighborhoods. Refer to `neighborhood_summary.csv` for exact values.
The chart includes 24 neighborhoods with at least 20 sales; the four omitted from the chart are Landmrk (n=1), GrnHill (n=2), Greens (n=8), Blueste (n=10). Their statistics remain in the CSV.

## Missing values and data checks

There are 719 blank cells in 21 columns (whitespace-only cells are counted as blank). The previous report's 510 total was an arithmetic error: the listed counts sum to 719, including 490 blank Lot Frontage cells and 159 blank Garage Yr Blt cells. Those two columns alone sum to 649.
Blank counts by column: Lot Frontage: 490; Mas Vnr Type: 23; Mas Vnr Area: 23; Bsmt Qual: 1; Bsmt Cond: 1; Bsmt Exposure: 4; BsmtFin Type 1: 1; BsmtFin SF 1: 1; BsmtFin Type 2: 2; BsmtFin SF 2: 1; Bsmt Unf SF: 1; Total Bsmt SF: 1; Electrical: 1; Bsmt Full Bath: 2; Bsmt Half Bath: 2; Garage Yr Blt: 159; Garage Finish: 2; Garage Cars: 1; Garage Area: 1; Garage Qual: 1; Garage Cond: 1.
The literal string `NA` appears 13,278 times across 14 columns, separate from blanks. It appears frequently in feature fields where it commonly indicates that a feature is absent (for example, Alley, Pool QC, Fence, and Misc Feature). The script preserves these as recorded and does not treat them as missing for the price comparison.
Literal `NA` counts by column: Alley: 2732; Bsmt Qual: 79; Bsmt Cond: 79; Bsmt Exposure: 79; BsmtFin Type 1: 79; BsmtFin Type 2: 79; Fireplace Qu: 1422; Garage Type: 157; Garage Finish: 157; Garage Qual: 158; Garage Cond: 158; Pool QC: 2917; Fence: 2358; Misc Feature: 2824.

## Outliers and interpretation

Using the overall 1.5 times IQR rule as a descriptive flag, the upper fence is $339,500.00 and 137 sales exceed it. These are retained in every statistic. Neighborhood mean and range can be sensitive to extreme prices, so the median and quartiles are the primary comparison measures.
The summaries are descriptive and unadjusted. Differences may reflect home size, quality, age, sale year, sale condition, or sale type as well as neighborhood. The chart's 20-sale threshold improves readability but does not imply that smaller groups are invalid; estimates for low-count neighborhoods are less stable. A later explanatory analysis should consider those property and transaction characteristics before interpreting neighborhood differences as independent effects.

## Reproducibility

Run `python analysis/neighborhood_analysis.py` from the repository root. The script uses only the Python standard library and writes the CSV, SVG chart, and this report in `analysis/`.
