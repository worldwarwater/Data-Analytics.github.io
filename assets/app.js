(function () {
  'use strict';
  var D = window.PORTFOLIO_DATA;
  var charts = {};

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  var fmt = {
    usd: function (v) { return '$' + Math.round(v).toLocaleString(); },
    k: function (v) { return '$' + Math.round(v / 1000) + 'K'; },
    pct: function (v) { return v + '%'; },
    num: function (v) { return Number(v).toLocaleString(); }
  };

  // ---------- Theme ----------
  var toggle = document.getElementById('theme-toggle');
  toggle.addEventListener('click', function () {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark' ||
      (!document.documentElement.getAttribute('data-theme') && matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    redrawAll();
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redrawAll);

  // ---------- Hero stats ----------
  var total = D.churn.n + D.jobs.n + D.marketing.n + D.books.n;
  var stats = [
    [total.toLocaleString(), 'records analyzed across projects'],
    ['6', 'end-to-end projects'],
    ['3', 'live Looker Studio dashboards'],
    ['3', 'languages: Python, SQL, R']
  ];
  document.getElementById('hero-stats').innerHTML = stats.map(function (s) {
    return '<div class="stat"><b>' + s[0] + '</b><span>' + s[1] + '</span></div>';
  }).join('');

  document.querySelectorAll('[data-bind]').forEach(function (el) {
    var path = el.getAttribute('data-bind').split('.');
    el.textContent = D[path[0]][path[1]];
  });

  // ---------- Filters ----------
  var chips = document.querySelectorAll('#filters .chip');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('active'); });
      chip.classList.add('active');
      var f = chip.getAttribute('data-filter');
      var shown = 0;
      document.querySelectorAll('.project').forEach(function (p) {
        var match = f === 'all' || p.getAttribute('data-tags').split(' ').indexOf(f) !== -1;
        p.hidden = !match;
        if (match) shown++;
      });
      document.getElementById('empty-msg').hidden = shown > 0;
      Object.keys(charts).forEach(function (k) { charts[k].chart && charts[k].chart.resize(); });
    });
  });

  // ---------- Chart helpers ----------
  function baseOptions(o) {
    var text = css('--text-secondary'), grid = css('--grid');
    var horizontal = o.horizontal;
    var valueAxis = {
      beginAtZero: true,
      grid: { color: grid, drawTicks: false },
      border: { display: false },
      ticks: { color: text, padding: 6, callback: function (v) { return o.tick ? o.tick(v) : v; } },
      title: o.axisTitle ? { display: true, text: o.axisTitle, color: text } : { display: false }
    };
    var catAxis = {
      grid: { display: false },
      border: { color: grid },
      ticks: { color: text, autoSkip: false, maxRotation: 0, font: { size: 12 } }
    };
    return {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: horizontal ? 'y' : 'x',
      animation: { duration: 350 },
      plugins: {
        legend: { display: !!o.legend, labels: { color: text, usePointStyle: true, boxWidth: 8 } },
        tooltip: {
          backgroundColor: css('--surface-1'), titleColor: css('--text-primary'), bodyColor: css('--text-primary'),
          borderColor: css('--border'), borderWidth: 1, padding: 10,
          callbacks: o.tooltip ? { label: o.tooltip } : {}
        }
      },
      scales: horizontal ? { x: valueAxis, y: catAxis } : { x: catAxis, y: valueAxis }
    };
  }

  function bar(labels, values, o) {
    var c1 = css('--series-1'), muted = css('--series-1-muted');
    return {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: o.highlight ? values.map(function (_, i) { return o.highlight(i) ? c1 : muted; }) : c1,
          borderRadius: 4,
          borderSkipped: 'start',
          maxBarThickness: 34,
          categoryPercentage: 0.8,
          barPercentage: 0.9
        }]
      },
      options: baseOptions(o),
      plugins: o.plugins || []
    };
  }

  function render(key, canvasId, configFn) {
    var entry = charts[key] || (charts[key] = {});
    entry.canvasId = canvasId;
    entry.configFn = configFn;
    if (entry.chart) entry.chart.destroy();
    entry.chart = new Chart(document.getElementById(canvasId), configFn());
  }
  function redrawAll() {
    Object.keys(charts).forEach(function (k) { render(k, charts[k].canvasId, charts[k].configFn); });
  }

  // Reference line plugin (overall churn)
  function refLine(value) {
    return {
      id: 'refLine',
      afterDatasetsDraw: function (chart) {
        var y = chart.scales.y.getPixelForValue(value), a = chart.chartArea, ctx = chart.ctx;
        ctx.save();
        ctx.strokeStyle = css('--text-secondary');
        ctx.setLineDash([5, 4]);
        ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(a.left, y); ctx.lineTo(a.right, y); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = css('--text-secondary');
        ctx.font = '12px system-ui, sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText('Overall ' + value + '%', a.right, y - 6);
        ctx.restore();
      }
    };
  }

  // ---------- Marketing ----------
  var M = D.marketing;
  var mktViews = {
    spend: function () {
      return bar(M.segments.labels, M.segments.spend, { horizontal: true, tick: fmt.usd, axisTitle: 'Average total spend per customer',
        tooltip: function (c) { return ' ' + fmt.usd(c.raw) + ' avg spend'; } });
    },
    resp: function () {
      return bar(M.segments.labels, M.segments.resp, { horizontal: true, tick: fmt.pct, axisTitle: 'Response rate to latest campaign',
        tooltip: function (c) { return ' ' + c.raw + '% responded'; } });
    },
    share: function () {
      return bar(M.segments.labels, M.segrev, { horizontal: true, tick: fmt.pct, axisTitle: 'Share of total customer spend',
        highlight: function (i) { return M.segrev[i] > 20; },
        tooltip: function (c) { return ' ' + c.raw + '% of all spend'; } });
    },
    n: function () {
      return bar(M.segments.labels, M.segments.n, { horizontal: true, tick: fmt.num, axisTitle: 'Customers',
        tooltip: function (c) { return ' ' + fmt.num(c.raw) + ' customers'; } });
    },
    scatter: function () {
      var pts = function (r) {
        return M.scatter.filter(function (p) { return p[2] === r; }).map(function (p) { return { x: p[0], y: p[1] }; });
      };
      var o = baseOptions({ legend: true });
      o.scales = {
        x: { grid: { color: css('--grid') }, border: { display: false }, ticks: { color: css('--text-secondary'), callback: fmt.k },
             title: { display: true, text: 'Annual income', color: css('--text-secondary') } },
        y: { grid: { color: css('--grid') }, border: { display: false }, ticks: { color: css('--text-secondary'), callback: fmt.usd },
             title: { display: true, text: 'Total spend (2 years)', color: css('--text-secondary') } }
      };
      o.plugins.tooltip.callbacks = { label: function (c) { return ' Income ' + fmt.usd(c.raw.x) + ', spend ' + fmt.usd(c.raw.y); } };
      var ring = css('--surface-1');
      return {
        type: 'scatter',
        data: { datasets: [
          { label: 'Did not respond', data: pts(0), backgroundColor: css('--series-1'), borderColor: ring, borderWidth: 1, pointRadius: 4, pointHoverRadius: 6 },
          { label: 'Responded to latest campaign', data: pts(1), backgroundColor: css('--series-2'), borderColor: ring, borderWidth: 1, pointRadius: 4, pointHoverRadius: 6 }
        ] },
        options: o
      };
    }
  };
  wireSeg('mkt', 'mkt-chart', mktViews, 'spend');

  var tbl = '<thead><tr><th>Test</th><th>Statistic</th><th>p-value</th><th>Effect size</th><th>Significant</th></tr></thead><tbody>' +
    M.tests.map(function (r) {
      r = r.slice();
      if (parseFloat(r[2]) < 0.001) r[2] = '&lt; 0.001'; else r[2] = String(Math.round(parseFloat(r[2]) * 1000) / 1000);
      return '<tr>' + r.map(function (c, i) { return '<td>' + (i === 2 ? c : c.replace(/[<>&]/g, '')) + '</td>'; }).join('') + '</tr>';
    }).join('') + '</tbody>';
  document.getElementById('mkt-tests').innerHTML = tbl;

  // ---------- Churn ----------
  var C = D.churn;
  var dimSel = document.getElementById('churn-dim');
  function churnChart() {
    var d = C.dims[dimSel.value];
    var max = Math.max.apply(null, d.rate);
    return bar(d.labels, d.rate, {
      tick: fmt.pct, axisTitle: 'Churn rate',
      highlight: function (i) { return d.rate[i] === max; },
      tooltip: function (c) { return ' ' + c.raw + '% churned (' + fmt.num(d.n[c.dataIndex]) + ' customers)'; },
      plugins: [refLine(C.rate)]
    });
  }
  dimSel.addEventListener('change', function () { render('churn', 'churn-chart', churnChart); });
  render('churn', 'churn-chart', churnChart);

  var slider = document.getElementById('mtm-slider');
  function calc() {
    var pct = +slider.value;
    var moved = C.mtm.n * pct / 100;
    var saved = moved * (C.mtm.rate - C.mtm.annual) / 100;
    document.getElementById('mtm-pct').textContent = pct;
    document.getElementById('mtm-cust').textContent = Math.round(saved).toLocaleString();
    document.getElementById('mtm-rev').textContent = fmt.usd(saved * C.mtm.charge);
  }
  slider.addEventListener('input', calc);
  calc();

  // ---------- Jobs ----------
  var J = D.jobs;
  var jobViews = {
    paying: function () {
      return bar(J.paying.labels, J.paying.values, { horizontal: true, tick: fmt.k, axisTitle: 'Average salary of postings listing the skill',
        tooltip: function (c) { return ' ' + fmt.usd(c.raw) + ' avg salary'; } });
    },
    demand: function () {
      return bar(J.demand.labels, J.demand.values, { horizontal: true, tick: fmt.num, axisTitle: 'Postings mentioning the skill (of ' + J.n.toLocaleString() + ')',
        tooltip: function (c) { return ' ' + c.raw + ' postings (' + Math.round(c.raw / J.n * 100) + '%)'; } });
    },
    experience: function () {
      return bar(J.experience.labels, J.experience.values, { tick: fmt.k, axisTitle: 'Average salary',
        tooltip: function (c) { return ' ' + fmt.usd(c.raw); } });
    },
    title: function () {
      return bar(J.title.labels, J.title.values, { horizontal: true, tick: fmt.k, axisTitle: 'Average salary',
        tooltip: function (c) { return ' ' + fmt.usd(c.raw); } });
    },
    worktype: function () {
      return bar(J.worktype.labels, J.worktype.applicants, { tick: fmt.num, axisTitle: 'Average applicants per posting',
        highlight: function (i) { return J.worktype.labels[i] === 'Remote'; },
        tooltip: function (c) { return [' ' + c.raw + ' applicants on average', ' ' + fmt.usd(J.worktype.salary[c.dataIndex]) + ' average salary']; } });
    }
  };
  wireSeg('jobs', 'jobs-chart', jobViews, 'paying');

  // ---------- Books ----------
  render('books', 'books-chart', function () {
    return bar(D.books.labels, D.books.values, { tick: fmt.num, axisTitle: 'Books',
      tooltip: function (c) { return ' ' + c.raw + ' books'; } });
  });

  // ---------- Segmented control wiring ----------
  function wireSeg(name, canvasId, views, initial) {
    var group = document.querySelector('.seg[data-chart="' + name + '"]');
    var buttons = group.querySelectorAll('button');
    buttons.forEach(function (b) {
      b.setAttribute('role', 'tab');
      b.addEventListener('click', function () {
        buttons.forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-selected', 'false'); });
        b.classList.add('active');
        b.setAttribute('aria-selected', 'true');
        render(name, canvasId, views[b.getAttribute('data-view')]);
      });
    });
    render(name, canvasId, views[initial]);
  }
})();
