(function () {
  var fmtPct = function (value) {
    return (Number(value) * 100).toFixed(Number(value) === 1 ? 0 : 1) + "%";
  };

  fetch("assets/data/site_data.v1.json")
    .then(function (response) { return response.json(); })
    .then(function (data) {
      var a = data.headline_results.frame_a;
      var b = data.headline_results.frame_b;
      var scenarios = Number(a.scenarios_scored) + Number(b.scenarios_scored);
      document.getElementById("metric-scenarios").textContent = String(scenarios);
      document.getElementById("metric-frame-a").textContent = a.passed + "/" + a.substantive_denominator;
      document.getElementById("metric-frame-b").textContent = b.passed + "/" + b.substantive_denominator;
      var labels = document.querySelectorAll(".metric__label");
      labels[0].textContent = "scenarios: " + a.scenarios_scored + " consumer + " + b.scenarios_scored + " business";
      labels[1].textContent = "Frame A final judge pass, " + fmtPct(a.pass_rate);
      labels[2].textContent = "Frame B final judge pass, " + fmtPct(b.pass_rate);
    })
    .catch(function () {
      // Static fallback values remain in the markup.
    });
})();
