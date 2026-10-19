"""Summarize Ames housing sale prices by neighborhood using only the stdlib.

Run from any directory with: python analysis/neighborhood_analysis.py
The script reads the repository CSV and writes a summary CSV, an SVG chart,
and a findings note alongside this file. No records are removed.
"""

import csv
import html
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def quantile(values, p):
    """Linear-interpolated quantile (same convention as NumPy's default)."""
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def money(value):
    return f"${value:,.2f}"


def write_chart(rows, path):
    # Keep small neighborhoods visible in the summary table; chart only n >= 20.
    shown = sorted((r for r in rows if r["sales"] >= 20), key=lambda r: r["median"], reverse=True)
    width, left, right, top, row_h = 1120, 160, 120, 58, 29
    height = top + row_h * len(shown) + 54
    max_value = max(r["median"] for r in shown)
    plot_width = width - left - right
    ticks = [0, 50000, 100000, 150000, 200000, 250000, 300000, 350000]
    scale_max = 350000
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#222}.title{font-size:22px;font-weight:bold}.label{font-size:14px}.tick{font-size:12px;fill:#555}.grid{stroke:#ddd;stroke-width:1}.bar{fill:#3977a8}</style>',
        f'<text x="{width / 2}" y="30" text-anchor="middle" class="title">Median sale price by neighborhood (20+ sales)</text>',
    ]
    for tick in ticks:
        x = left + plot_width * tick / scale_max
        parts.append(f'<text x="{x:.1f}" y="{height-20}" text-anchor="middle" class="tick">${tick//1000}k</text>')
    for i, r in enumerate(shown):
        y = top + i * row_h
        bar_w = plot_width * r["median"] / scale_max
        parts.append(f'<text x="{left-10}" y="{y+17}" text-anchor="end" class="label">{html.escape(r["neighborhood"])} (n={r["sales"]})</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="20" rx="2" class="bar"/>')
        parts.append(f'<text x="{left+bar_w+7:.1f}" y="{y+15}" class="tick">${r["median"]:,.0f}</text>')
    parts.append('</svg>')
    path.write_text('\n'.join(parts), encoding='utf-8')


def main():
    candidates = [ROOT / "AmesHousing.csv", ROOT / "AmesHousing-1.csv"]
    source = next((p for p in candidates if p.exists()), None)
    if source is None:
        raise FileNotFoundError("Expected AmesHousing.csv or AmesHousing-1.csv in repository root")

    with source.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        data = list(reader)
        fields = reader.fieldnames or []
    required = {"Neighborhood", "SalePrice", "Sale Condition", "Sale Type"}
    missing_fields = required.difference(fields)
    if missing_fields:
        raise ValueError(f"CSV is missing required columns: {sorted(missing_fields)}")

    blanks = {field: sum(not (row.get(field) or "").strip() for row in data) for field in fields}
    blanks = {field: count for field, count in blanks.items() if count}
    literal_na = {field: sum((row.get(field) or "").strip() == "NA" for row in data) for field in fields}
    literal_na = {field: count for field, count in literal_na.items() if count}

    groups = {}
    for row_num, row in enumerate(data, start=2):
        neighborhood = (row.get("Neighborhood") or "").strip()
        if not neighborhood:
            raise ValueError(f"Blank Neighborhood at CSV row {row_num}")
        try:
            price = float(row["SalePrice"])
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid SalePrice at CSV row {row_num}: {row.get('SalePrice')!r}") from error
        groups.setdefault(neighborhood, []).append(price)

    results = []
    for neighborhood, prices in groups.items():
        results.append({
            "neighborhood": neighborhood,
            "sales": len(prices),
            "median": statistics.median(prices),
            "mean": statistics.mean(prices),
            "min": min(prices),
            "q1": quantile(prices, 0.25),
            "q3": quantile(prices, 0.75),
            "max": max(prices),
        })
    results.sort(key=lambda row: (row["median"], row["neighborhood"]))

    summary_path = OUT / "neighborhood_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["Neighborhood", "Sales", "Median Sale Price", "Mean Sale Price", "Minimum Sale Price", "First Quartile Sale Price", "Third Quartile Sale Price", "Maximum Sale Price"])
        writer.writeheader()
        for row in results:
            writer.writerow({
                "Neighborhood": row["neighborhood"], "Sales": row["sales"],
                "Median Sale Price": f'{row["median"]:.2f}', "Mean Sale Price": f'{row["mean"]:.2f}',
                "Minimum Sale Price": f'{row["min"]:.2f}', "First Quartile Sale Price": f'{row["q1"]:.2f}',
                "Third Quartile Sale Price": f'{row["q3"]:.2f}', "Maximum Sale Price": f'{row["max"]:.2f}',
            })

    chart_path = OUT / "median_sale_price_by_neighborhood.svg"
    write_chart(results, chart_path)

    low_n = sorted((r for r in results if r["sales"] < 20), key=lambda r: r["sales"])
    top = max(results, key=lambda r: r["median"])
    bottom = min(results, key=lambda r: r["median"])
    overall_prices = [float(row["SalePrice"]) for row in data]
    # IQR rule is used only to describe potential extremes; no rows are excluded.
    q1, q3 = quantile(overall_prices, .25), quantile(overall_prices, .75)
    upper_fence = q3 + 1.5 * (q3 - q1)
    high_count = sum(price > upper_fence for price in overall_prices)
    note = [
        "# Neighborhood sale price findings", "",
        f"Source: `{source.name}` ({len(data):,} sales, {len(fields)} variables). All valid sale records are retained.", "",
        f"Across all neighborhoods, the median sale price is {money(statistics.median(overall_prices))}; the mean is {money(statistics.mean(overall_prices))}. Neighborhood medians range from {money(bottom['median'])} in {bottom['neighborhood']} (n={bottom['sales']}) to {money(top['median'])} in {top['neighborhood']} (n={top['sales']}).",
        "", "## Neighborhood patterns", "",
        "The complete summary table reports the number of sales, median, mean, minimum, first quartile, third quartile, and maximum for all 28 neighborhoods. Refer to `neighborhood_summary.csv` for exact values.",
        f"The chart includes {sum(r['sales'] >= 20 for r in results)} neighborhoods with at least 20 sales; the four omitted from the chart are " + ", ".join(f"{r['neighborhood']} (n={r['sales']})" for r in low_n) + ". Their statistics remain in the CSV.",
        "", "## Missing values and data checks", "",
        f"There are {sum(blanks.values()):,} blank cells in {len(blanks)} columns (whitespace-only cells are counted as blank). The previous report's 510 total was an arithmetic error: the listed counts sum to 719, including 490 blank Lot Frontage cells and 159 blank Garage Yr Blt cells. Those two columns alone sum to 649.",
        "Blank counts by column: " + "; ".join(f"{name}: {count}" for name, count in blanks.items()) + ".",
        f"The literal string `NA` appears {sum(literal_na.values()):,} times across {len(literal_na)} columns, separate from blanks. It appears frequently in feature fields where it commonly indicates that a feature is absent (for example, Alley, Pool QC, Fence, and Misc Feature). The script preserves these as recorded and does not treat them as missing for the price comparison.",
        "Literal `NA` counts by column: " + "; ".join(f"{name}: {count}" for name, count in literal_na.items()) + ".",
        "", "## Outliers and interpretation", "",
        f"Using the overall 1.5 times IQR rule as a descriptive flag, the upper fence is {money(upper_fence)} and {high_count} sales exceed it. These are retained in every statistic. Neighborhood mean and range can be sensitive to extreme prices, so the median and quartiles are the primary comparison measures.",
        "The summaries are descriptive and unadjusted. Differences may reflect home size, quality, age, sale year, sale condition, or sale type as well as neighborhood. The chart's 20-sale threshold improves readability but does not imply that smaller groups are invalid; estimates for low-count neighborhoods are less stable. A later explanatory analysis should consider those property and transaction characteristics before interpreting neighborhood differences as independent effects.",
        "", "## Reproducibility", "",
        "Run `python analysis/neighborhood_analysis.py` from the repository root. The script uses only the Python standard library and writes the CSV, SVG chart, and this report in `analysis/`.",
    ]
    (OUT / "neighborhood_findings.md").write_text("\n".join(note) + "\n", encoding="utf-8")

    print(f"Source: {source.name}")
    print(f"Loaded {len(data)} observations and {len(fields)} variables; summarized {len(results)} neighborhoods.")
    print(f"Blank cells: {sum(blanks.values())} across {len(blanks)} columns; literal NA entries: {sum(literal_na.values())} across {len(literal_na)} columns.")
    print(f"Chart includes {sum(r['sales'] >= 20 for r in results)} neighborhoods (sales >= 20); outlier sales retained.")
    print(f"Wrote {summary_path.name}, {chart_path.name}, neighborhood_findings.md")


if __name__ == "__main__":
    main()
