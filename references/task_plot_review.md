# Task Plot Review

## Evidence Match

- Pass: title and construct match the Dictator Game.
- Pass: rows match configured low, medium, and high stake conditions.
- Pass: phase order matches README and `src/run_trial.py`: Stake prompt -> Fixation -> Allocation decision -> Choice feedback -> Outcome feedback -> ITI.
- Pass: timing labels match config: 600 ms stake prompt, 500 ms fixation, 2200 ms decision, 500 ms choice feedback, 1000 ms outcome feedback, 800 ms ITI.
- Pass: decision key mapping shows F generous, SPACE equal, and J selfish.
- Pass: allocation options show generous/equal/selfish self ratios and feedback shows self/other amounts and totals.
- Pass: no partner response stage is shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
