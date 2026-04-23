/* ns-tooltip.js — wiki-style hover glossary for Neurosteer Physician Guide */
(function () {
  'use strict';

  // ── TERMS DICTIONARY ──────────────────────────────────────────
  // Each entry: { full, desc, pub? }
  // pub = publications.html anchor id, shown as clickable "View publication" link
  var NS_TERMS = {
    // ── Clinical / scoring terms ──────────────────────────────
    'MMSE': {
      full: 'Mini-Mental State Examination',
      desc: '30-point pen-and-paper cognitive screening test. Scores: ≥28 healthy, 24–27 borderline/MCI range, <24 mild dementia.'
    },
    'MoCA': {
      full: 'Montreal Cognitive Assessment',
      desc: '30-point screening tool; broader domain coverage than MMSE, more sensitive to mild impairment.'
    },
    'MCI': {
      full: 'Mild Cognitive Impairment',
      desc: 'Early cognitive decline beyond normal aging but not meeting dementia criteria. MMSE typically 24–27.'
    },
    'HRV': {
      full: 'Heart Rate Variability',
      desc: 'Beat-to-beat variation in heart rate. Higher HRV indicates stronger parasympathetic tone and lower physiological stress.'
    },
    'PNN50': {
      full: 'pNN50 — Percentage of NN50 Intervals',
      desc: 'HRV metric: % of consecutive RR-intervals differing >50 ms. Higher values indicate parasympathetic (relaxed) dominance.',
      pub: 'pub-maimon-2025-stress'
    },
    'SDNN': {
      full: 'SDNN — Standard Deviation of NN Intervals',
      desc: 'Overall HRV metric reflecting total autonomic variability. Validated against AS (ST4) in Neurosteer cortisol-HRV cohort.',
      pub: 'pub-maimon-2025-stress'
    },
    'RMSSD': {
      full: 'Root Mean Square of Successive Differences',
      desc: 'Short-term HRV metric reflecting parasympathetic modulation. Shown alongside PNN50 in the AS–HRV validation.'
    },
    'HPA': {
      full: 'Hypothalamic–Pituitary–Adrenal Axis',
      desc: 'Neuroendocrine system governing cortisol secretion in response to stress. Chronic activation blunts acute NE recruitment.',
      pub: 'pub-maimon-2026-field'
    },
    'EEG': {
      full: 'Electroencephalography',
      desc: 'Non-invasive measurement of electrical brain activity via scalp electrodes. Neurosteer uses a single prefrontal channel.'
    },
    'hdrEEG': {
      full: 'High-Density Resolution EEG™',
      desc: 'Neurosteer\'s proprietary signal processing pipeline combining wavelet-packet decomposition with ML feature extraction on a single frontal electrode.'
    },
    'EFA': {
      full: 'Executive Function Age',
      desc: 'Neurosteer composite score estimating cognitive brain age. Derived from NE, ME, and AS markers; validated against MMSE across 977 participants.',
      pub: 'pub-molcho-2025'
    },
    'TBR': {
      full: 'Theta/Beta Ratio',
      desc: 'Frontal EEG ratio of theta (4–8 Hz) to beta (13–30 Hz) power. Elevated in attention dysregulation.'
    },
    'BAR': {
      full: 'Beta Arousal Ratio',
      desc: 'High-frequency EEG power ratio reflecting stress reactivity. Correlated with pre-session cortisol (r = −0.42) in Neurosteer cohort.'
    },
    'LC-NE': {
      full: 'Locus Coeruleus – Norepinephrine System',
      desc: 'Brainstem circuit governing cognitive alertness and arousal. Its degeneration explains absent CA (L1) task-activation in both Parkinson\'s and early dementia.',
      pub: 'pub-molcho-2023-pd'
    },
    'tDCS': {
      full: 'Transcranial Direct Current Stimulation',
      desc: 'Non-invasive brain stimulation applying weak direct current to modulate cortical excitability.',
      pub: 'pub-maimon-2022-bci'
    },
    'DOC': {
      full: 'Disorder of Consciousness',
      desc: 'Severe impairment of wakefulness or awareness (e.g., vegetative state, minimally conscious state).',
      pub: 'pub-maimon-2022-bci'
    },
    'CLT': {
      full: 'Cognitive Load Theory',
      desc: 'Framework describing working memory capacity limits under task demands. Used in the laparoscopic surgery training study.',
      pub: 'pub-maimon-2022-lap'
    },
    'STAI': {
      full: 'State–Trait Anxiety Inventory',
      desc: 'Validated self-report measure distinguishing immediate (state) from chronic (trait) anxiety levels.'
    },
    'LMM': {
      full: 'Linear Mixed Model',
      desc: 'Statistical model handling repeated measures and individual variability. Primary inference method across all Neurosteer EEG studies.'
    },
    'PET': {
      full: 'Positron Emission Tomography',
      desc: 'Nuclear imaging measuring metabolic or neurochemical activity. F-DOPA PET is the standard for early Parkinson\'s screening.',
      pub: 'pub-molcho-2023-pd'
    },
    'SNR': {
      full: 'Signal-to-Noise Ratio',
      desc: 'Ratio of meaningful signal amplitude to background noise. Single-channel EEG achieves high SNR via Neurosteer\'s wavelet decomposition.'
    },
    // ── Neurosteer feature names ──────────────────────────────
    'NE': {
      full: 'Neural Efficiency',
      desc: 'Cognitive resource allocation marker (A0). Increases with load in healthy adults; blunted in MCI and dementia. Strongest MMSE correlation: r ≈ −0.44.',
      pub: 'pub-molcho-2025'
    },
    'CA': {
      full: 'Cognitive Alertness',
      desc: 'Noradrenergic alertness marker (L1). Healthy and MCI: clear rest→task activation. Mild Dementia and F-DOPA+ Parkinson\'s: activation absent — shared LC-NE mechanism.',
      pub: 'pub-molcho-2023-pd'
    },
    'ME': {
      full: 'Memory Engagement',
      desc: 'Working memory load marker (VC9). Increases monotonically with N-back level in healthy participants; sensitive to early WM decline.',
      pub: 'pub-maimon-2021-wm'
    },
    'AS': {
      full: 'Arousal & Stress',
      desc: 'Physiological stress-at-rest marker (ST4). Cross-validated with HRV: PNN50 r = −0.34, SDNN r = −0.24.',
      pub: 'pub-maimon-2025-stress'
    },
    'SR': {
      full: 'Stress Reactivity',
      desc: 'Acute stress response marker (T2). Negatively correlated with self-reported calmness; elevated under high task demand.',
      pub: 'pub-maimon-2025-dissoc'
    },
  };

  // ── PUB REFERENCES (for data-pub cite spans & figure captions) ─
  var PUB_REFS = {
    'pub-molcho-2025': {
      short: 'Molcho et al. (2025)',
      venue: 'Scientific Reports',
      title: 'Automated frontal single-channel EEG cognitive screening'
    },
    'pub-molcho-2023-pd': {
      short: 'Molcho et al. (2023)',
      venue: 'Frontiers in Neurology',
      title: 'EEG-based Parkinson\'s early diagnosis via auditory cognitive assessment'
    },
    'pub-maimon-2022-lap': {
      short: 'Maimon et al. (2022)',
      venue: 'Frontiers in Neuroscience',
      title: 'Mental load monitoring during laparoscopic surgery simulation'
    },
    'pub-molcho-2022': {
      short: 'Molcho et al. (2022)',
      venue: 'Frontiers in Aging Neuroscience',
      title: 'Single-channel EEG features reveal cognitive decline in seniors'
    },
    'pub-maimon-2025-ichci': {
      short: 'Maimon et al. (2025)',
      venue: 'IEEE ICHCI 2025',
      title: 'Neural dissociation of cognitive load, arousal, and stress'
    },
    'pub-maimon-2022-bci': {
      short: 'Maimon et al. (2022)',
      venue: 'IEEE BCI 2022',
      title: 'EEG reactivity changes following tDCS in DOC patients'
    },
    'pub-maimon-2021-wm': {
      short: 'Maimon et al. (2021)',
      venue: 'IEEE LifeTech 2021',
      title: 'Novel single-channel EEG features correlate with working memory load'
    },
    'pub-bolton-2021': {
      short: 'Bolton et al. (2021)',
      venue: 'IEEE LifeTech 2021',
      title: 'Detecting interruption events using single-channel frontal EEG'
    },
    'pub-maimon-2025-stress': {
      short: 'Maimon et al. (2025)',
      venue: 'arXiv preprint',
      title: 'Personalized stress detection via hdrEEG, cortisol, and HRV'
    },
    'pub-maimon-2025-dissoc': {
      short: 'Maimon et al. (2025)',
      venue: 'arXiv preprint',
      title: 'Dissociating cognitive load and stress responses with single-channel EEG'
    },
    'pub-yahalom-2025': {
      short: 'Yahalom et al. (2025)',
      venue: 'arXiv preprint',
      title: 'Breathing 5:5 effect on resilience and stress via single-channel EEG'
    },
    'pub-maimon-2026-field': {
      short: 'Maimon et al. (2026)',
      venue: 'SSRN preprint',
      title: 'Neural dissociation of cognitive effort and physiological arousal — field study'
    },
  };

  // ── CREATE TOOLTIP ELEMENT ─────────────────────────────────────
  var tip = document.createElement('div');
  tip.id = 'ns-tooltip';
  document.body.appendChild(tip);

  var hideTimer = null;

  function buildHTML(key, pubId) {
    var html = '';
    var linkId = pubId;

    if (key && NS_TERMS[key]) {
      var t = NS_TERMS[key];
      html += '<div class="tt-term">' + key + '</div>';
      html += '<div class="tt-full">' + t.full + '</div>';
      html += '<div class="tt-desc">' + t.desc + '</div>';
      if (!linkId) linkId = t.pub;
    }

    if (linkId && PUB_REFS[linkId]) {
      var p = PUB_REFS[linkId];
      if (!key) {
        // pure pub-cite span — show paper info
        html += '<div class="tt-full">' + p.short + '</div>';
        html += '<div class="tt-desc">' + p.title + '. <em>' + p.venue + '</em></div>';
      }
      html += '<a class="tt-pub-link" href="publications.html#' + linkId + '" target="_blank">'
             + '↗ ' + p.short + ' — ' + p.venue + '</a>';
    }

    return html;
  }

  function showTip(el) {
    clearTimeout(hideTimer);
    var key = el.dataset.key || null;
    var pubId = el.dataset.pub || null;
    var html = buildHTML(key, pubId);
    if (!html) return;
    tip.innerHTML = html;
    tip.classList.add('visible');
    positionTip(el);
  }

  function positionTip(el) {
    var rect = el.getBoundingClientRect();
    var margin = 8;
    var top = rect.bottom + margin + window.scrollY;
    var left = rect.left + window.scrollX;
    var tipW = 300;
    if (left + tipW > window.innerWidth - 16) left = window.innerWidth - tipW - 16;
    if (left < 8) left = 8;
    tip.style.top = top + 'px';
    tip.style.left = left + 'px';
  }

  function scheduleHide() {
    hideTimer = setTimeout(function () { tip.classList.remove('visible'); }, 200);
  }

  tip.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
  tip.addEventListener('mouseleave', scheduleHide);

  // ── EVENT DELEGATION ──────────────────────────────────────────
  document.addEventListener('mouseover', function (e) {
    var el = e.target.closest ? e.target.closest('.ns-gloss') : null;
    if (el) showTip(el);
  });
  document.addEventListener('mouseout', function (e) {
    var el = e.target.closest ? e.target.closest('.ns-gloss') : null;
    if (el) scheduleHide();
  });

  // ── AUTO-GLOSS: wrap known terms in text nodes ─────────────────
  var SCAN_TERMS = Object.keys(NS_TERMS).sort(function (a, b) { return b.length - a.length; });

  // Build case-sensitive regex: match only when not preceded/followed by a letter
  var escapedTerms = SCAN_TERMS.map(function (t) {
    return t.replace(/[-.*+?^${}()|[\]\\]/g, '\\$&');
  });
  var termRe = new RegExp('(?<![A-Za-z])(' + escapedTerms.join('|') + ')(?![A-Za-z])', 'g');

  var SKIP_TAGS = { A: 1, BUTTON: 1, SCRIPT: 1, STYLE: 1, CODE: 1, PRE: 1, TEXTAREA: 1, INPUT: 1, SELECT: 1 };

  function glossNode(node) {
    var text = node.nodeValue;
    termRe.lastIndex = 0;
    if (!termRe.test(text)) return;
    termRe.lastIndex = 0;

    var frag = document.createDocumentFragment();
    var last = 0, m;
    while ((m = termRe.exec(text)) !== null) {
      if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
      var span = document.createElement('span');
      span.className = 'ns-gloss';
      span.dataset.key = m[1];
      span.textContent = m[1];
      frag.appendChild(span);
      last = m.index + m[1].length;
    }
    if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
    node.parentNode.replaceChild(frag, node);
  }

  function walkNode(node) {
    if (node.nodeType === 3) { // TEXT_NODE
      var p = node.parentNode;
      if (p && !SKIP_TAGS[p.tagName] && !(p.classList && p.classList.contains('ns-gloss'))) {
        glossNode(node);
      }
      return;
    }
    if (node.nodeType !== 1) return; // not ELEMENT_NODE
    if (SKIP_TAGS[node.tagName]) return;
    var kids = Array.from(node.childNodes);
    for (var i = 0; i < kids.length; i++) walkNode(kids[i]);
  }

  function init() {
    var main = document.querySelector('.main');
    if (main) walkNode(main);
    // activate any manually placed data-pub spans
    document.querySelectorAll('[data-pub]').forEach(function (el) {
      if (!el.classList.contains('ns-gloss')) el.classList.add('ns-gloss');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 0);
  }
})();
