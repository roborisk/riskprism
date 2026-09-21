---
layout: default
title: "RiskPrism: Aligning Visual Evidence for Physical Risk Reasoning in Vision-Language Models"
subtitle: 'Aligning Visual Evidence for Physical Risk Reasoning<br>in Vision-Language Models'
description: "A benchmark and practical techniques for aligning visual evidence for physical risk reasoning in vision-language models."
---

<section class="hero" id="top" data-nav="Overview">
  <div class="wrap">
    <figure class="frame" style="margin:0 auto">
      <video autoplay muted loop playsinline controls preload="auto"
             poster="{{ '/assets/images/teaser.jpg' | relative_url }}">
        <source src="{{ '/assets/videos/riskprismpromo.mp4' | relative_url }}" type="video/mp4">
      </video>
    </figure>
    <figcaption>An overview of the benchmark, our visual prompting and test-time ensembling techniques, and closed-loop deployment on a Boston Dynamics Spot.</figcaption>
  </div>
</section>

<!-- ===================== TEASER + ABSTRACT ===================== -->
<section id="abstract">
  <div class="wrap" markdown="1">

<figure class="teaser">
  <a href="{{ '/assets/pdf/teaser.pdf' | relative_url }}">
    <img src="{{ '/assets/images/teaser.jpg' | relative_url }}"
         alt="A quadruped in a warehouse with three candidate paths coloured by risk level, and two annotated hazards.">
  </a>
  <figcaption><strong>Figure 1.</strong> Field environments offer many geometrically feasible paths that differ enormously in risk. Here the green path keeps clear of both a loose cable run (Hazard 1) and a lit hazard zone beneath an active scissor lift (Hazard 2), while the red path crosses both. RiskPrism scores each candidate path against natural-language operator preferences and returns a single scalar risk cost that a planner can consume directly.</figcaption>
</figure>

## Abstract

Assessing motion planning risk in complex, unstructured environments remains challenging. Vision-language models (VLMs) can provide open-set visual semantic understanding, but it remains an open question what capacity these models have for assessing navigation risk. In this work, we systematically evaluate and improve VLM risk assessment without task-specific fine-tuning. We introduce the largest real-world risk understanding benchmark in unstructured industrial environments, consisting of **109 robot deployments across 15 unique job sites**, from factories to construction sites. We further propose several practical, broadly effective techniques for improving risk reasoning across a variety of VLMs: a novel **visual prompting** technique that explicitly projects future motion plans onto past visual memory, and **test-time ensembling** for tail risk estimation, which together improve reliability under real-world perception and environment uncertainty. Across our offline benchmark and 120 real-world experiments spanning diverse operational hazard types, our techniques consistently improve risk estimation accuracy for lethal hazards by **45%** across closed and open-source VLMs, and reduce real-world deployment interventions by **27%**. To support future research on risk understanding, we release our evaluation benchmark, code, and additional deployment videos.

  </div>
</section>

<!-- ===================== BENCHMARK ===================== -->
<section id="benchmark">
  <div class="wrap" markdown="1">

<p class="section-kicker">Benchmark</p>
## A risk reasoning benchmark grounded in real field deployments.

Progress on risk reasoning has been held back by the absence of data where risk is both *labelled* and *conditioned on stated preferences*. Our benchmark is built from **109 robot deployments across 15 unique job sites**, from factories to active construction sites, and annotated through a purpose-built tool that keeps the labeller in the same observation context the model will see at test time.

<div class="pills">
  <span class="pill">Transparent barriers</span>
  <span class="pill">Deformables</span>
  <span class="pill">Keep-out zones</span>
  <span class="pill">Negative obstacles</span>
  <span class="pill">Social interactions</span>
</div>

**Hazards that geometry cannot see.** The benchmark deliberately concentrates on five hazard families that defeat conventional traversability estimation. Glass walls and railings register as free space; cable bundles and mats are geometrically traversable but carry tangle and slip risk; cones and caution tape are semantic, not physical, barriers; floor openings appear only a few frames before they matter; and people at work require standoff that no occupancy grid encodes.

<figure class="fig-single wide">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/benchmark-hazards.pdf' | relative_url }}">
      <img src="{{ '/assets/images/benchmark-hazards.jpg' | relative_url }}"
           alt="Grid of field imagery grouped into five hazard categories: transparent barriers, deformables, keepout zones, negative obstacles, and social interactions.">
    </a>
  </div>
  <figcaption><strong>Figure 2.</strong> Representative observations from each of the five hazard families in the benchmark. Every category is under-served by purely geometric traversability estimation, and each is labelled under preferences that state how the operator wants that hazard treated.</figcaption>
</figure>

**Labelling with Visual Verification.** Annotators work inside a tool that shows the candidate path set overlaid on the current observation, the projected paths across the preceding frames of visual memory, and a bird's-eye-view cost map with the accumulated plan. Risk ratings are assigned per candidate path on a 1–5 scale, alongside the relevant natural-language risk preferences for that clip.

<figure class="fig-single">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/benchmark-labeling-tool.pdf' | relative_url }}">
      <img src="{{ '/assets/images/benchmark-labeling-tool.png' | relative_url }}"
           alt="Screenshot of the annotation tool showing path candidates, a video scrubber, per-path risk selection, preference selection, visual memory frames, and a bird's-eye-view cost map.">
    </a>
  </div>
  <figcaption><strong>Figure 3.</strong> The annotation interface. Labellers see all sampled path candidates on the current frame, scrub the underlying video, assign a 1–5 risk rating per path, and attach the natural-language preferences that apply — with the projected visual memory and BEV cost map visible throughout.</figcaption>
</figure>

**Judgements that require more than one view.** A substantial fraction of the benchmark cannot be resolved from a single frame. In the example below, whether a path respects the instruction *"stay in the area indicated by construction marker posts"* only becomes decidable once the marker posts seen several frames earlier are carried forward, which is precisely the capability the visual-memory projection is designed to supply.

<figure class="fig-single wide">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/benchmark-multiview.pdf' | relative_url }}">
      <img src="{{ '/assets/images/benchmark-multiview.jpg' | relative_url }}"
           alt="Three consecutive robot views of a construction walkway with candidate paths overlaid and the instruction to stay within construction marker posts.">
    </a>
  </div>
  <figcaption><strong>Figure 4.</strong> A multi-view case. The same candidate path is ambiguous from the latest frame alone; the marker posts that define the permitted corridor are only visible in earlier observations.</figcaption>
</figure>

<figure class="fig-single tall">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/benchmark-statistics.pdf' | relative_url }}">
      <img src="{{ '/assets/images/benchmark-statistics.png' | relative_url }}"
           alt="Two stacked bar charts: trajectory arc length distribution coloured by risk rating, and risk ratings broken down by hazard type.">
    </a>
  </div>
  <figcaption><strong>Figure 5.</strong> Benchmark composition. <em>Top:</em> trajectory arc length against risk rating — risk is spread across path lengths rather than confounded with them, and an extended-length split stresses longer-horizon reasoning. <em>Bottom:</em> candidate labels per hazard type, showing that every family contains both clearly safe and clearly lethal paths.</figcaption>
</figure>

  </div>
</section>

<!-- ===================== APPROACH ===================== -->
<section id="approach">
  <div class="wrap" markdown="1">

<p class="section-kicker">Approach</p>
## Project the path into visual memory, then reason about the tail.

Both of our techniques operate entirely at inference time — no task-specific fine-tuning, and nothing that ties them to a particular VLM. The pipeline takes a visual memory <em>O</em><sub>t</sub> of recent egocentric observations, a set of natural-language preferences <em>P</em>, and a candidate trajectory <em>T</em>, and returns a scalar risk cost <em>y</em> that a downstream planner can add to its objective.

**Visual prompting over past observations.** The candidate trajectory is projected back into each frame of the visual memory, so the model reasons about the path against every observation in which the relevant hazard was visible, not only the latest one. This is what makes hazards that have since left the field of view — a ditch the robot has already walked past, marker posts behind the current heading — still count against a path.

**Test-time ensembling for tail risk.** Rather than asking for one rating, we ensemble risk ratings sampled across the projected views and fit a tail-risk distribution over them. A single risk-tolerance parameter <em>&alpha;</em> selects how much of the upper tail the final cost reflects: <em>&alpha;</em>&nbsp;=&nbsp;0 recovers the expected rating, while larger <em>&alpha;</em> weights the worst outcomes the model considers plausible. Operators get one dial with a clear meaning instead of an opaque threshold.

<figure class="fig-single wide">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/approach.pdf' | relative_url }}">
      <img src="{{ '/assets/images/approach.jpg' | relative_url }}"
           alt="Pipeline diagram: visual memory, preferences, and a trajectory feed a multiview projection stage, then a tail risk estimation stage that fits a distribution over sampled risks and emits a scalar risk cost.">
    </a>
  </div>
  <figcaption><strong>Figure 6.</strong> The RiskPrism pipeline. Visual memory, natural-language preferences, and a candidate trajectory are the only inputs. The trajectory is projected into each past observation, a VLM samples risk ratings per view, and a tail-risk distribution parameterised by the tolerance <em>&alpha;</em> is reduced to a single scalar risk cost.</figcaption>
</figure>

  </div>
</section>

<!-- ===================== OFFLINE RESULTS ===================== -->
<section id="results" data-nav="Results">
  <div class="wrap" markdown="1">

<p class="section-kicker">Offline evaluation</p>
## Fewer catastrophic underestimates, at the same overall error budget.

The metric that matters for deployment is not average rating error but *asymmetric* error: overestimating risk makes a robot timid, while underestimating it damages the robot or the site. We therefore report underestimation <em>U</em> and overestimation <em>O</em> separately, and compare against learned traversability baselines (Slowfast, Slowfast with hybrid projection) and the VLM-based FORTRESS.

<div class="headline">
  <div class="h">
    <div class="v">109</div>
    <div class="k">robot deployments across 15 unique industrial job sites.</div>
  </div>
  <div class="h">
    <div class="v">45%</div>
    <div class="k">better lethal-hazard risk estimation, across closed and open-source VLMs.</div>
  </div>
  <div class="h">
    <div class="v">27%</div>
    <div class="k">fewer operator interventions in real-world deployment.</div>
  </div>
</div>

### The safety frontier.

Sweeping the risk-tolerance parameter traces a frontier in the (<em>O</em>,&nbsp;<em>U</em>) plane, and every backbone we test moves down and to the left when tail-risk estimation replaces single-shot rating. The gain is not a relabelling of the same predictions: closed-source and open-source models alike cross to a lower mean-absolute-error contour, and the sweep exposes the operating point choice explicitly rather than burying it in a threshold.

### Where the errors land.

Broken down by hazard type, the baselines underestimate exactly where underestimation is most costly. FORTRESS understates risk on transparent barriers and dynamic entities by a wide margin; the Slowfast variants trade that for heavy overestimation. Our approach keeps both sides bounded and is 45% better at estimating lethal hazard risks on the full benchmark, and the advantage holds on the extended-path-length split.

<div class="figpair">
  <figure>
    <div class="imgwrap">
      <a href="{{ '/assets/pdf/results-safety-frontier.pdf' | relative_url }}">
        <img src="{{ '/assets/images/results-safety-frontier.png' | relative_url }}"
             alt="Scatter plot of underestimation versus overestimation with MAE contours, showing each backbone moving toward the lower-left with our method.">
      </a>
    </div>
    <figcaption><strong>Figure 7.</strong> Safety-frontier trade-off. Each curve sweeps the risk-tolerance parameter <em>&alpha;</em> &isin; {0, 0.25, 0.5, 0.75, 0.9}; crosses are baselines. Lower-left is better. Every backbone improves over its single-shot counterpart.</figcaption>
  </figure>
  <figure>
    <div class="imgwrap">
      <a href="{{ '/assets/pdf/results-misprediction.pdf' | relative_url }}">
        <img src="{{ '/assets/images/results-misprediction.png' | relative_url }}"
             alt="Diverging bar chart of underestimation and overestimation rates per method, split by hazard type and path length.">
      </a>
    </div>
    <figcaption><strong>Figure 8.</strong> Misprediction rate split into underestimation (left) and overestimation (right), by hazard type and by path length. Baselines buy low overestimation with dangerous underestimation; our approach keeps both sides bounded.</figcaption>
  </figure>
</div>

<!-- Replace the TBD cells with the final numbers from the paper. -->
<!-- <div class="tblwrap">
  <table class="tbl">
    <caption><strong>Table 1.</strong> Headline offline results on the full benchmark. <em>U</em> and <em>O</em> are underestimation and overestimation rates; lower is better throughout. Best row in colour.</caption>
    <thead>
      <tr>
        <th>Method</th>
        <th class="num">MAE</th>
        <th class="num">U (%)</th>
        <th class="num">O (%)</th>
        <th class="num">Lethal U (%)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>FORTRESS</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td></tr>
      <tr><td>Slowfast</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td></tr>
      <tr><td>Slowfast (Hybrid Proj.)</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td></tr>
      <tr class="divider"><td>RiskPrism (no tail risk, &alpha; = 0)</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td></tr>
      <tr class="best"><td>RiskPrism (full, &alpha; = 0.5)</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td><td class="num">TBD</td></tr>
    </tbody>
  </table>
</div> -->

### Qualitative comparison.

The same scene, scored by every method. Slowfast produces sparse, unstable path scores and loses the hazard as the robot advances; the hybrid-projection variant recovers geometry but reads the debris field as clear; FORTRESS marks nearly the whole fan as safe. RiskPrism carries the hazard forward across all four observations and keeps every path that crosses the debris in the high-risk band.

<figure class="fig-single wide">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/results-qualitative.pdf' | relative_url }}">
      <img src="{{ '/assets/images/results-qualitative.jpg' | relative_url }}"
           alt="Four rows comparing Slowfast, Slowfast with hybrid projection, FORTRESS, and our approach across four timesteps of the same scene, with candidate paths coloured by predicted risk.">
    </a>
  </div>
  <figcaption><strong>Figure 9.</strong> Qualitative comparison across four timesteps of the same episode (rows: Slowfast, Slowfast + hybrid projection, FORTRESS, RiskPrism). Path colour encodes predicted risk, green for low and red for high. Only RiskPrism keeps the hazard scored consistently once it leaves the centre of the field of view.</figcaption>
</figure>

  </div>
</section>

<!-- ===================== REAL-ROBOT EXPERIMENTS ===================== -->
<section id="real-robot" data-nav="Robot experiments">
  <div class="wrap" markdown="1">

<p class="section-kicker">Real-robot experiments</p>
## Closed-loop deployment on a Spot quadruped.

We attach the predicted risk cost to the planner on a Boston Dynamics Spot and run 120 real-world experiments across three scenarios that isolate distinct preference types: a **keep-out** constraint, an explicit **hazard-avoidance** instruction, and a **keep-in** corridor constraint. Each scenario is driven only by the natural-language preference shown beneath the clip — no scenario-specific tuning, no hand-authored cost regions. Across these deployments our techniques reduce operator interventions by 27%. Every clip below runs fully autonomously at 5&times; speed and is shown side by side against a baseline, with the baseline's failure called out as it happens.

<figure class="fig-single wide">
  <div class="imgwrap">
    <a href="{{ '/assets/pdf/realworld-scenarios.pdf' | relative_url }}">
      <img src="{{ '/assets/images/realworld-scenarios.jpg' | relative_url }}"
           alt="Three real-world scenarios with executed robot paths overlaid: keep out zones, hazard avoidance, and keep in zones.">
    </a>
  </div>
  <figcaption><strong>Figure 10.</strong> The three deployment scenarios with the executed trajectory overlaid. <em>Left:</em> keep-out zones marked with caution tape and cones. <em>Middle:</em> hazard avoidance around tangle-risk cords. <em>Right:</em> a keep-in corridor defined by striped lane markings.</figcaption>
</figure>

  </div>

  <div class="wrap-wide">
    <div class="video-block">
      <div class="video-row">

        <div class="vcard">
          <video autoplay muted loop playsinline controls preload="metadata" data-autoplay>
            <source src="{{ '/assets/videos/keepout_comparison.mp4' | relative_url }}" type="video/mp4">
          </video>
          <div class="vmeta">
            <h4>Keep-Out Zones</h4>
            <p class="quote">&ldquo;Stay on the left side of the caution tape. Avoid cone keepout areas.&rdquo;</p>
            <p>The baseline underestimates clearance to the keepout zone and clips the cone line; our risk cost holds the executed path outside it.</p>
          </div>
        </div>

        <div class="vcard">
          <video autoplay muted loop playsinline controls preload="metadata" data-autoplay>
            <source src="{{ '/assets/videos/avoidance_comparison.mp4' | relative_url }}" type="video/mp4">
          </video>
          <div class="vmeta">
            <h4>Hazard Avoidance</h4>
            <p class="quote">&ldquo;Do not step over caution tape. Do not step on cords that clearly tangle risks. Avoid cone keepout areas.&rdquo;</p>
            <p>Three simultaneous constraints of different types. Slowfast backtracks at the caution-tape barrier, while our tail-risk cost keeps the cord run high-risk even as it slides out of view.</p>
          </div>
        </div>

        <div class="vcard">
          <video autoplay muted loop playsinline controls preload="metadata" data-autoplay>
            <source src="{{ '/assets/videos/keepin_comparison.mp4' | relative_url }}" type="video/mp4">
          </video>
          <div class="vmeta">
            <h4>Keep-In Zones</h4>
            <p class="quote">&ldquo;Stay within the striped lane markings. Avoid stepping on cords that are tangle risks. Keep out of cone areas.&rdquo;</p>
            <p>A positive corridor constraint rather than a negative one. The baseline fails to detect the loose striped tape boundary and leaves the lane; ours stays inside while avoiding the cord hazard within it.</p>
          </div>
        </div>

      </div>
    </div>
  </div>
</section>

<!-- ===================== GAUNTLET ===================== -->
<section id="gauntlet" data-nav="RiskPrism Gauntlet">
  <div class="wrap" markdown="1">

<p class="section-kicker">Long-horizon deployment</p>
## The RiskPrism Gauntlet.

The three scenarios above isolate one preference type each. The Gauntlet chains all of them into a single uninterrupted run: the robot leaves a keep-out zone, negotiates tangle-risk cords and a caution-tape barrier, and finishes inside a marked lane — with no reset and no operator input between scenes. It is the hardest test we run, because a single underestimated hazard ends the episode.

<figure class="fig-single wide clip">
  <div class="imgwrap">
    <video muted loop playsinline controls preload="metadata"
           poster="{{ '/assets/images/gauntlet-poster.jpg' | relative_url }}">
      <source src="{{ '/assets/videos/looped_gauntlet_full5x.mp4' | relative_url }}" type="video/mp4">
    </video>
  </div>
  <figcaption><strong>The RiskPrism Gauntlet.</strong> A single fully autonomous run across all three scenes, played at 5&times; speed (3&nbsp;min 29&nbsp;s). The inset shows candidate paths projected into visual memory and coloured by predicted risk; the bar along the bottom tracks progress through the three scenes.</figcaption>
</figure>

  </div>
</section>

<!-- ===================== CITATION ===================== -->
<section id="citation">
  <div class="wrap" markdown="1">

<p class="section-kicker">Citation</p>
## If RiskPrism is useful in your work, please cite us.

<div class="bib">
<button class="copybtn" data-target="bibtex" type="button">Copy</button><span id="bibtex">{% raw %}@inproceedings{anonymous2026riskprism,
  title     = {RiskPrism: Aligning Visual Evidence for Physical Risk Reasoning in Vision-Language Models},
  author    = {Anonymous Authors},
  booktitle = {Under Review},
  year      = {2026},
}{% endraw %}</span>
</div>

  </div>
</section>
