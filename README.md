# Tokopedia Smartphone Market Dynamics & Pricing Strategy

An end-to-end data analytics project evaluating pricing dispersion, specification extraction, brand competitive positioning, and storage efficiency (Price-per-GB) across 2,200+ smartphone listings on Tokopedia using Python.

---

## Executive Summary

* **Decentralized Brand Landscape:** The market demonstrates heavy segmentation. Budget brands like `Infinix` and `Xiaomi` saturate the entry-level spectrum (< Rp2M), while `Samsung` exhibits the most resilient multi-tier diversification across all brackets.
* **Storage Cost Disparity (Value-for-Money):** Hardware storage margins vary dramatically. `Infinix` delivers the most aggressive consumer storage efficiency at a median of **Rp15,525 per GB**, whereas `Apple` commands a steep premium at **Rp59,367 per GB** (~3.8x premium margin), reflecting brand equity and iOS ecosystem lock-in.
* **High-Density Mid-Range Clustering:** Mid-tier devices (`Rp2M – Rp5M`) represent the most contested battlefield. Brands like `Poco`, `Vivo`, and `Realme` compress tight interquartile price ranges with high RAM/ROM offerings to capture volume.
* **Regex Pipeline Resilience:** Achieved an **82.3% (1,859 units)** extraction rate for Internal Storage (ROM) and **60.8% (1,373 units)** for RAM directly from unstructured, seller-defined listing titles.

---

## Executive Visualizations

### 1. Price Tier Distribution by Brand
![Price Tier Distribution](./figures/1_price_tier_distribution.png)

* **Market Share Footprint:** `Samsung` maintains an active footprint across every pricing tier, acting as the benchmark competitor from budget to ultra-flagship. `Apple` exclusively monopolizes the Flagship tier (> Rp10M) with zero presence in budget categories for new retail units.
* **Volume Anchors:** `Infinix`, `Xiaomi/Redmi`, and `Vivo` drive bulk volume in the Sub-5M segments, validating high price sensitivity among mass-market consumers.

---

### 2. Price Dispersion & Outlier Analysis (Logarithmic Scale)
![Price Range Boxplot](./figures/2_price_range_boxplot.png)

* **Variance Spread:** Log-scale distribution confirms substantial interquartile ranges (IQR) for `Apple` and `Samsung`, driven by distinct tier segmentation (base models vs. Pro/Ultra variants).
* **Segment Discipline:** Value-focused manufacturers maintain tight, predictable price bands, avoiding cannibalization across product iterations.

---

### 3. Storage Efficiency Metric (Median Price per GB)
![Storage Efficiency](./figures/3_value_per_gb_storage.png)

* **Hardware Utility:** Median cost per gigabyte exposes direct hardware margins. `Infinix` (Rp15,525/GB), `Vivo` (Rp18,485/GB), and `Xiaomi` (Rp19,133/GB) offer maximum storage utility per rupiah.
* **Ecosystem Surcharge:** `Apple` trades at a massive premium, demonstrating that consumer willingness to pay is decoupled from raw hardware cost and tied directly to ecosystem retention.

---

## Business Insights & Strategic Recommendations

* **OEM Positioning:** Brands competing in the Rp2M – Rp5M tier must differentiate via secondary specifications (fast charging, display tech) as storage-per-rupiah metrics have reached parity.
* **Catalog Standardization:** E-commerce platforms suffer substantial search leakage due to arbitrary naming conventions; implementing forced attribute drop-downs could increase match conversion by reducing unmapped variants.

---

## Data Architecture & Methods

* **Ingestion:** Automated dynamic Chromium crawler targeting 44 category-defining smartphone keywords with lazy-load event triggers and strict hardware blacklist filters.
* **Feature Engineering:** Regex-driven extraction pipeline parsing non-standard storage tokens (`RAM/ROM`, `Extended RAM`, `TB conversion`) and categorical binning across 4 distinct price tiers.
