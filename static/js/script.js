/* ════════════════════════════════════════════
   RetailIQ — script.js
   jQuery + Chart.js + form validation
   ════════════════════════════════════════════ */

$(document).ready(function () {

  /* ── 1. Discount range display ──────────── */
  const $range = $("#discountRange");
  const $val   = $("#discVal");
  function updateDiscount() { $val.text($range.val() + "%"); }
  $range.on("input", updateDiscount);
  updateDiscount();

  /* ── 2. Client-side form validation ────── */
  $("#predictForm").on("submit", function (e) {
    $("#clientErrors").remove();
    const msgs = [];
    const category = $("#category").val();
    const month    = $("#month").val();
    const units    = $("input[name='units_sold']").val().trim();
    const price    = $("input[name='price']").val().trim();
    const disc     = parseFloat($range.val());

    if (!category)  msgs.push("Please select a product category.");
    if (!month)     msgs.push("Please select a month.");
    if (!units || isNaN(units) || parseInt(units) <= 0)
      msgs.push("Units sold must be a positive whole number.");
    if (!price || isNaN(price) || parseFloat(price) <= 0)
      msgs.push("Price must be a valid number greater than 0.");
    if (disc < 0 || disc > 100)
      msgs.push("Discount must be between 0% and 100%.");

    if (msgs.length) {
      e.preventDefault();
      const html = `<div class="alert-custom alert-error-custom mb-3" id="clientErrors">
        <div class="alert-icon alert-icon-error"><i class="bi bi-exclamation-triangle-fill"></i></div>
        <div><div class="alert-title">Fix these errors:</div>
        ${msgs.map(m => `<div class="alert-body">• ${m}</div>`).join('')}</div></div>`;
      $("#predictForm").prepend(html);
      $("html,body").animate({ scrollTop: $("#predict-section").offset().top - 80 }, 400);
      return;
    }

    $("#btnText").addClass("d-none");
    $("#btnSpinner").removeClass("d-none");
    $("#submitBtn").prop("disabled", true);
  });

  /* ── 3. Charts ──────────────────────────── */
  $.getJSON("/api/chart-data", function (d) {
    drawMonthChart(d);
    drawCatChart(d);
    drawUnitsChart(d);
  });

  const GREEN  = "rgba(22,163,74,1)";
  const GREENB = "rgba(22,163,74,0.12)";
  const BLUES  = ["#2563eb","#db2777","#ea580c","#0891b2","#16a34a"];
  const BLUESA = ["rgba(37,99,235,.75)","rgba(219,39,119,.75)","rgba(234,88,12,.75)","rgba(8,145,178,.75)","rgba(22,163,74,.75)"];

  Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
  Chart.defaults.color = "#6b6b80";

  function drawMonthChart(d) {
    const ctx = document.getElementById("monthChart");
    if (!ctx) return;
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: d.month_labels,
        datasets: [{
          label: "Revenue (₹)",
          data: d.month_revenue,
          backgroundColor: GREENB,
          borderColor: GREEN,
          borderWidth: 2,
          borderRadius: 8,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#1a1a2e",
            titleColor: "#fff",
            bodyColor: "#a3a3b5",
            padding: 10,
            callbacks: {
              label: ctx => " ₹" + ctx.parsed.y.toLocaleString("en-IN", {maximumFractionDigits:0})
            }
          }
        },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 12 } } },
          y: {
            grid: { color: "rgba(0,0,0,.05)" },
            ticks: {
              font: { size: 12 },
              callback: v => "₹" + (v/1000).toFixed(0) + "k"
            }
          }
        }
      }
    });
  }

  function drawCatChart(d) {
    const ctx = document.getElementById("catChart");
    if (!ctx) return;
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: d.category_labels,
        datasets: [{
          data: d.category_revenue,
          backgroundColor: BLUESA,
          borderColor: "#ffffff",
          borderWidth: 3,
          hoverOffset: 8,
        }]
      },
      options: {
        responsive: true,
        cutout: "60%",
        plugins: {
          legend: {
            position: "bottom",
            labels: { boxWidth: 11, padding: 12, font: { size: 11 } }
          },
          tooltip: {
            backgroundColor: "#1a1a2e",
            callbacks: {
              label: ctx => " ₹" + ctx.parsed.toLocaleString("en-IN",{maximumFractionDigits:0})
            }
          }
        }
      }
    });
  }

  function drawUnitsChart(d) {
    const ctx = document.getElementById("unitsChart");
    if (!ctx) return;
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: d.category_labels,
        datasets: [{
          label: "Units Sold",
          data: d.category_units,
          backgroundColor: BLUESA,
          borderColor: BLUES,
          borderWidth: 1.5,
          borderRadius: 6,
          borderSkipped: false,
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#1a1a2e",
            callbacks: {
              label: ctx => " " + ctx.parsed.x.toLocaleString() + " units"
            }
          }
        },
        scales: {
          x: { grid: { color: "rgba(0,0,0,.05)" }, ticks: { font: { size: 12 } } },
          y: { grid: { display: false }, ticks: { font: { size: 12 } } }
        }
      }
    });
  }

  /* ── 4. Smooth scroll ───────────────────── */
  $("a[href^='#']").on("click", function (e) {
    const target = $(this.getAttribute("href"));
    if (target.length) {
      e.preventDefault();
      $("html,body").animate({ scrollTop: target.offset().top - 72 }, 480);
    }
  });

  /* ── 5. Auto-dismiss success banner ─────── */
  setTimeout(function () {
    $("#successBanner").fadeOut(500, function () { $(this).remove(); });
  }, 7000);

  /* ── 6. Animate rank bars on scroll ─────── */
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.rank-bar-fill').forEach(bar => {
          const w = bar.style.width;
          bar.style.width = '0%';
          setTimeout(() => { bar.style.width = w; }, 100);
        });
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('#top-products .row').forEach(row => observer.observe(row));

});
