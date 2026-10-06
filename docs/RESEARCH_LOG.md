# RESEARCH_LOG — sequential multi-tool voting (2026-10-06 UTC)

One search at a time (no parallel websearch; backoff on 429; DuckDuckGo-lite fallback).
Distinct keywords per tool to collect different opinions.

1. websearch (Exa): "Galileo inclined plane bells odd numbers 1 3 5 7 ..." → Museo Galileo 5-bell plane; IMEKO 2025-113 + Roma3 PDF (11/33/55/77cm, Audacity/Tracker); Acta IMEKO water-clock ±0.1s needs repetition+stats; PhysicsLAB ramps.
2. searxng_web_search: "Newton Principia 1687 ..." → NETWORK ERROR (SEARXNG_URL unavailable). Documented; fell back to other tools per protocol.
3. openresearch web_search: "Newton cannon orbital velocity 7.9 km/s ..." → cannonball Wikipedia; Weber State simulator; NovaSolver/ZenCalculators 2026-07 explainers.
4. paper-search search_papers (arxiv,semantic,openalex): "double slit electron single particle ..." → Coles 1403.4687 entropic WPDR; Bach 2013 controlled double-slit (188 cites); Rabinowitz physics/0302062 review.
5. duckduckgo_search (web): "Maxwell equations speed of light ..." → 10 hits: Wikipedia, OpenStax 24.1, GeeksforGeeks, c=1/sqrt(mu0 eps0) derivations.
6. openresearch search_openalex: "Standard Model 17 particles Higgs ..." → Chung mass formulas; Gunion-Haber; LEP Higgs 114.4 GeV bound.
7. websearch: "special relativity 1905 time dilation light clock E=mc2 muons GPS" → NIST 2025-04-03; Ashby PMC5253894 (NTS-2 +442.5 vs +446.5e-12; +38us/d); BU light-clock PDF; UCL muon GM+RPi lab; Gutenberg Einstein Relativity.
8. agent-reach_search (web): "reproducible physics research Docker benchmarking open science 2026" → monstr FAIR chain 2604.25944; Apptainer HEP 2604.06244; Guix+Apptainer 2512.13826; FAIR4HEP cookiecutter; CERN reproducibility/REANA/Snakemake; Collider-Bench; Frontiers 2024 review; FORRT template.
9. wiki_search: "general relativity spacetime curvature experimental tests" → Curved spacetime; Tests of GR; GR; Minkowski; Intro to GR.
10. kaggle search_everything: "physics inclined plane orbital mechanics benchmark datasets" → NO RESULTS (gap this repo fills).
11. openresearch search_news: "quantum gravity dark matter dark energy unsolved physics 2026" → Space.com 2026-09-07 quantum-gravity analogue; MSN/DC piece (noise).
12. paper-search search_arxiv: "entropy second law statistical mechanics irreversibility" → Wallace 2104.11223; Nelson 2401.02977; Bhattacharjee 2609.23850 (2026, error 0.001); Matsuoka withdrawn (honest negative).
13. gsd_websearch: "best reproducible science Docker Compose Python benchmark live data verification 2026" → empty output (documented).
14. openresearch hacker_news: "reproducible science docker physics simulation open data" → no results (documented).
15. openresearch get_current_date → 2026-10-06T09:47:27Z (anchor).
16. openresearch get_crypto_price BTC 7d → 83583–86417 range (seed for cache).
17. openresearch get_fx_rate USD→EUR 0.89254 GBP 0.75616 JPY 158.23 (2026-10-05).
18. agent-reach stock_quote AAPL → 332.89, vol 34328912 (yfinance).
19. gitmcp search_generic_documentation FAIR4HEP/cookiecutter4fair → no indexed docs; fallback returned repo structure (used for layout).
20. kaggle models_list "physics simulation" → 5 models (ADC, Majorana, MOD SPACE H2, Mirror_OS, NexaHEP) — no direct benchmark reuse.
21. wiki get_summary "Tests of general relativity" → Mercury/light-bending/redshift; 1919, 1954, 1959 program.
22. superpowers recommend_skills → writing-skills/systematic-debugging/writing-plans (used systematic verification mindset).
23. openresearch stackoverflow "python physics simulation test reproducible docker numpy" → no results.
24. paper-search search_semantic "orbital mechanics inverse square ..." → empty (documented).
25. kaggle datasets_list "physics experiment pendulum" → sort_by type error (documented API mismatch).
26. searxng search_suggestions "quantum double slit reproducibility benchmark" → empty list (service up, no suggestions).
27. webfetch lite.duckduckgo "Galileo inclined plane odd numbers ..." → 9 hits incl. odd-numbers Wikipedia, guidedphysics, 2026-07-25 video, ontological atlas, knowledgekingdom 2026-07-08.
28. openresearch europepmc "entropy thermodynamics statistical mechanics" → 4041 papers; Parrondo 2026; Diambra 2026; Jeynes 2026.
29. kaggle discussions_search "reproducible research benchmark open data" → 5 threads (SWE-Bench+, ChatBot Arena, OpenFWI...).
30. openresearch sec_filings "artificial intelligence risk disclosure 10-K" → AITX 8-K 2026-09-10 etc. (market-disclosure angle for live-data section).

Live re-verification at runtime (this repo): CoinGecko BTC 86047 (169 pts), Frankfurter FX identical to step 17, Yahoo AAPL 332.89 identical to step 18 — all `source: live`.

Best-practice synthesis applied: Git+review+CI, executable-state capture, HDF5/JSON metadata, pinned env (Docker), benchmark JSON, Zenodo-intent DOI, RO-Crate-compatible layout, Snakemake/REANA-ready single-command pipeline.
