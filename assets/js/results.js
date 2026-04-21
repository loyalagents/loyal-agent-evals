(function () {
  var state = {
    frames: [],
    rows: [],
    sort: "id"
  };

  var $ = function (id) { return document.getElementById(id); };
  var esc = function (value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  };
  var pct = function (value) {
    return (Number(value) * 100).toFixed(Number(value) === 1 ? 0 : 1) + "%";
  };
  var badgeClass = function (status) {
    if (status === "PASS") return "status-pass";
    if (status === "FAIL") return "status-fail";
    return "status-na";
  };
  var badge = function (status) {
    return '<span class="status-badge ' + badgeClass(status) + '">' + esc(status || "N/A") + "</span>";
  };
  var finalScore = function (row) {
    var finals = row.scores.filter(function (score) {
      return /semantic alignment|business compliance judge/i.test(score.stage_name || "");
    });
    return finals.length ? finals[finals.length - 1] : row.scores[row.scores.length - 1];
  };

  function renderSummary(siteData) {
    var cards = $("summary-cards");
    var a = siteData.headline_results.frame_a;
    var b = siteData.headline_results.frame_b;
    cards.innerHTML = [
      ["Frame A - Consumer", a],
      ["Frame B - Business", b]
    ].map(function (entry) {
      var title = entry[0];
      var h = entry[1];
      return '<article class="metric"><span class="metric__value">' +
        esc(h.passed + "/" + h.substantive_denominator) +
        '</span><span class="metric__label">' + esc(title) + " final-stage pass, " +
        esc(pct(h.pass_rate)) + ". " + esc(h.failed) + " failed, " + esc(h.errors) +
        " errors, " + esc(h.missing_outputs) + " missing outputs.</span></article>";
    }).join("");
  }

  function renderStages() {
    var html = state.frames.map(function (frame) {
      var title = frame.frame === "frame_a" ? "Frame A - Consumer" : "Frame B - Business";
      var rows = frame.stage_summary.map(function (s) {
        return "<tr><td>" + esc(title) + "</td><td>" + esc(s.stage_name) + "</td><td>" +
          esc(s.applicable_outputs) + "</td><td>" + esc(s.not_applicable_outputs) + "</td><td>" +
          esc(s.passed) + "</td><td>" + esc(s.failed) + "</td><td>" +
          esc(s.average_score == null ? "" : Number(s.average_score).toFixed(3)) + "</td></tr>";
      }).join("");
      return rows;
    }).join("");
    $("stage-body").innerHTML = html;
  }

  function renderDutyRollup() {
    var merged = {};
    state.frames.forEach(function (frame) {
      frame.duty_rollup.forEach(function (row) {
        var target = merged[row.duty] || { duty: row.duty, passed: 0, failed: 0, not_applicable: 0, applicable: 0, total: 0 };
        ["passed", "failed", "not_applicable", "applicable", "total"].forEach(function (key) {
          target[key] += Number(row[key] || 0);
        });
        merged[row.duty] = target;
      });
    });
    var rows = Object.keys(merged).sort().map(function (key) {
      var row = merged[key];
      var denom = Math.max(row.applicable, 1);
      var width = Math.round((row.passed / denom) * 100);
      return '<div class="bar-row"><strong>' + esc(row.duty) + '</strong><div class="bar-track"><span class="bar-fill" style="width:' +
        width + '%"></span></div><span>' + esc(row.passed + "/" + row.applicable) +
        " applicable pass; " + esc(row.not_applicable) + " N/A</span></div>";
    }).join("");
    $("duty-rollup").innerHTML = rows;
  }

  function buildRows() {
    state.rows = [];
    state.frames.forEach(function (frame) {
      var label = frame.frame === "frame_a" ? "Frame A" : "Frame B";
      frame.items.forEach(function (item) {
        state.rows.push({
          id: item.id,
          frame: frame.frame,
          frameLabel: label,
          input: item.input,
          output: item.output,
          scores: item.scores
        });
      });
    });
  }

  function populateFilters() {
    var scorers = {};
    state.rows.forEach(function (row) {
      row.scores.forEach(function (score) {
        scorers[score.stage_name || score.scorer_name] = true;
      });
    });
    $("scorer-filter").innerHTML = '<option value="all">All scorers</option>' +
      Object.keys(scorers).sort().map(function (name) {
        return '<option value="' + esc(name) + '">' + esc(name) + "</option>";
      }).join("");
    var params = new URLSearchParams(window.location.search);
    if (params.get("scenario")) {
      $("scenario-search").value = params.get("scenario");
    }
  }

  function rowMatches(row) {
    var frameValue = $("frame-filter").value;
    var scorerValue = $("scorer-filter").value;
    var statusValue = $("status-filter").value;
    var query = $("scenario-search").value.trim().toLowerCase();

    if (frameValue !== "all" && row.frame !== frameValue) return false;
    if (query && (row.id + " " + row.input).toLowerCase().indexOf(query) === -1) return false;
    if (scorerValue === "all" && statusValue === "all") return true;

    return row.scores.some(function (score) {
      var scorerMatch = scorerValue === "all" || (score.stage_name || score.scorer_name) === scorerValue;
      var statusMatch = statusValue === "all" || score.status === statusValue;
      return scorerMatch && statusMatch;
    });
  }

  function sortRows(rows) {
    if (state.sort === "score") {
      return rows.sort(function (a, b) {
        var as = finalScore(a).score;
        var bs = finalScore(b).score;
        if (as == null && bs == null) return a.id.localeCompare(b.id);
        if (as == null) return 1;
        if (bs == null) return -1;
        return Number(bs) - Number(as) || a.id.localeCompare(b.id);
      });
    }
    return rows.sort(function (a, b) { return a.id.localeCompare(b.id); });
  }

  function renderTable() {
    var rows = sortRows(state.rows.filter(rowMatches));
    $("row-count").textContent = rows.length + " of " + state.rows.length + " scenarios";
    $("scenario-body").innerHTML = rows.map(function (row) {
      var final = finalScore(row);
      var scoreBadges = row.scores.map(function (score) {
        return '<span title="' + esc(score.stage_name || score.scorer_name) + '">' + badge(score.status) + "</span>";
      }).join("");
      var detailRows = row.scores.map(function (score) {
        var scoreValue = score.score == null ? "N/A" : Number(score.score).toFixed(2);
        return "<tr><td>" + esc(score.stage_name || score.scorer_name) + "</td><td>" +
          badge(score.status) + "</td><td>" + esc(scoreValue) + "</td><td>" +
          esc(score.reasoning || "") + "</td></tr>";
      }).join("");
      return "<tr><td><strong>" + esc(row.id) + "</strong><br><span class=\"metric__label\">" +
        esc(row.input) + "</span></td><td>" + esc(row.frameLabel) + "</td><td>" +
        badge(final.status) + "<br><code>" + esc(final.score == null ? "N/A" : Number(final.score).toFixed(2)) +
        "</code></td><td><div class=\"score-list\">" + scoreBadges +
        "</div><details class=\"score-detail\"><summary>Score details</summary><p>" +
        esc(row.output || "") + "</p><div class=\"table-wrap\"><table><thead><tr><th>Stage</th><th>Status</th><th>Score</th><th>Reasoning</th></tr></thead><tbody>" +
        detailRows + "</tbody></table></div></details></td></tr>";
    }).join("");
  }

  Promise.all([
    fetch("../assets/data/site_data.v1.json").then(function (r) { return r.json(); }),
    fetch("../assets/data/frame_a.v1.json").then(function (r) { return r.json(); }),
    fetch("../assets/data/frame_b.v1.json").then(function (r) { return r.json(); })
  ]).then(function (payloads) {
    renderSummary(payloads[0]);
    state.frames = [payloads[1], payloads[2]];
    renderStages();
    renderDutyRollup();
    buildRows();
    populateFilters();
    renderTable();
    ["frame-filter", "scorer-filter", "status-filter", "scenario-search", "sort-select"].forEach(function (id) {
      $(id).addEventListener("input", function () {
        state.sort = $("sort-select").value;
        renderTable();
      });
    });
  }).catch(function (error) {
    $("results-error").hidden = false;
    $("results-error").textContent = "Results data failed to load: " + error.message;
  });
})();
