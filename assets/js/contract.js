(function () {
  var duties = {
    act: {
      label: "Duty to Act",
      high: "Provider shall ensure the agent carries out valid user instructions within authorized scope and records any refusal with a specific scope basis.",
      medium: "Agent should execute valid instructions within the authorization file and explain any refusal.",
      light: "Agent will try to complete authorized tasks and explain when it cannot."
    },
    loyalty: {
      label: "Duty of Loyalty",
      high: "Provider shall firewall compensation, referral, advertising, and ownership interests from recommendations unless disclosed and consented to by the user.",
      medium: "Agent must disclose material conflicts and avoid recommendations primarily driven by provider benefit.",
      light: "Agent should tell the user about conflicts that may affect a recommendation."
    },
    care: {
      label: "Duty of Care",
      high: "Provider shall maintain controls requiring competent execution, risk flagging before irreversible actions, and source-aware explanations for consequential recommendations.",
      medium: "Agent must use reasonable care, flag material uncertainty, and provide enough information for user review.",
      light: "Agent should be careful, explain uncertainty, and avoid obviously harmful actions."
    },
    obedience: {
      label: "Duty of Obedience",
      high: "Agent shall operate only inside the user's authorization file, decline illegal instructions, and cite the governing authorization limit when refusing.",
      medium: "Agent must follow authorized instructions and explain any scope limit.",
      light: "Agent should follow the user's stated limits."
    },
    disclosure: {
      label: "Duty of Disclosure",
      high: "Provider shall disclose conflicts, material limitations, data access, and action status in a durable audit trail before the user is bound.",
      medium: "Agent must disclose conflicts and important limits before proceeding.",
      light: "Agent should explain important limits and conflicts."
    },
    confirmation: {
      label: "Confirmation / UETA 10(b)",
      high: "For electronic transactions, agent must present a review-and-correct opportunity and obtain confirmation before finality unless a lawful exception is documented.",
      medium: "Agent must ask the user to confirm material transactions before finalizing.",
      light: "Agent should ask before purchases or other binding actions."
    },
    confidentiality: {
      label: "Confidentiality",
      high: "Provider shall use user data only to execute authorized tasks, prohibit unrelated model training without opt-in consent, and keep deletion and audit controls.",
      medium: "Agent must minimize data access and keep user data confidential.",
      light: "Agent should only use data needed for the task."
    },
    compliance: {
      label: "Compliance First",
      high: "When law conflicts with policy, profit, or convenience, the agent must prioritize legal compliance, document the basis, and escalate where legal judgment is required.",
      medium: "Agent must honor legal requirements over internal policy.",
      light: "Agent should not follow instructions that appear unlawful."
    },
    dual: {
      label: "Dual-Fiduciary Handling",
      high: "In dual-fiduciary settings, agent must acknowledge both principals' duties, use objective criteria, require mutual disclosure, and avoid unauthorized side deals.",
      medium: "Agent must recognize dual-fiduciary conflicts and seek fair objective criteria.",
      light: "Agent should disclose when both sides owe duties."
    }
  };

  var $ = function (id) { return document.getElementById(id); };

  function selectedDuties() {
    return Array.prototype.slice.call(document.querySelectorAll("[data-duty]:checked")).map(function (input) {
      return input.value;
    });
  }

  function generate() {
    var profile = $("duty-profile").value;
    var project = $("contract-project").value.trim() || "AI Agent Service";
    var selected = selectedDuties();
    var lines = [
      "# Observable Contractual Loyalty Stub",
      "",
      "**Project:** " + project,
      "**Duty profile:** " + profile,
      "",
      "> Example language only. Not legal advice. Adapt with counsel before using in production.",
      "",
      "## Parties and Authorization",
      "",
      "The user delegates bounded authority to the provider to operate an AI agent on the user's behalf. The agent may act only within the incorporated authorization file, including transaction limits, approved vendors, exclusions, data-access limits, and confirmation settings.",
      "",
      "## Selected Duty Modules",
      ""
    ];

    selected.forEach(function (key) {
      lines.push("### " + duties[key].label);
      lines.push("");
      lines.push(duties[key][profile]);
      lines.push("");
    });

    if (!selected.length) {
      lines.push("_No duty modules selected yet._", "");
    }

    lines.push("## Evaluation Hooks");
    lines.push("");
    lines.push("- Maintain logs sufficient to test duty performance.");
    lines.push("- Define scenario metadata for conflicts, legal requirements, ToS restrictions, confirmation gates, and dual-fiduciary settings.");
    lines.push("- Treat N/A as an explicit applicability verdict, not a pass or fail.");
    lines.push("");
    lines.push("## Reference Texts");
    lines.push("");
    lines.push("- CONTRACT.md");
    lines.push("- AUTH_PREFS.md");
    $("contract-output").value = lines.join("\n");
  }

  document.querySelectorAll("[data-duty], #duty-profile, #contract-project").forEach(function (el) {
    el.addEventListener("input", generate);
  });

  $("select-core-duties").addEventListener("click", function () {
    ["act", "loyalty", "care", "obedience", "disclosure", "confirmation"].forEach(function (key) {
      document.querySelector('[data-duty][value="' + key + '"]').checked = true;
    });
    generate();
  });

  $("copy-contract").addEventListener("click", function () {
    $("contract-output").select();
    navigator.clipboard.writeText($("contract-output").value).then(function () {
      $("copy-status").textContent = "Copied.";
    }).catch(function () {
      document.execCommand("copy");
      $("copy-status").textContent = "Copied.";
    });
  });

  generate();
})();
