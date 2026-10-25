document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".flash-close").forEach((button) => {
    button.addEventListener("click", () => button.closest(".flash")?.remove());
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm || "Are you sure?")) event.preventDefault();
    });
  });

  const backdrop = document.getElementById("task-modal");
  const form = document.getElementById("task-form");
  const title = document.getElementById("modal-title");
  const defaultAction = form?.getAttribute("action");
  const defaultHeading = "Add a new task";

  function openModal() {
    if (!backdrop) return;
    backdrop.classList.add("is-open");
    backdrop.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
    setTimeout(() => document.getElementById("task-title")?.focus(), 80);
  }
  function closeModal() {
    if (!backdrop) return;
    backdrop.classList.remove("is-open");
    backdrop.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
  }
  document.querySelectorAll("[data-open-modal]").forEach((button) => button.addEventListener("click", () => {
    resetTaskForm();
    openModal();
  }));
  document.querySelectorAll("[data-close-modal]").forEach((button) => button.addEventListener("click", closeModal));
  backdrop?.addEventListener("click", (event) => { if (event.target === backdrop) closeModal(); });
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeModal(); });

  function resetTaskForm() {
    if (!form) return;
    form.reset();
    form.action = defaultAction;
    if (title) title.textContent = defaultHeading;
    const category = document.getElementById("task-category");
    if (category) category.value = "General";
    const priority = document.getElementById("task-priority");
    if (priority) priority.value = "Medium";
    const status = document.getElementById("task-status");
    if (status) status.value = "Pending";
  }

  document.querySelectorAll("[data-edit-task]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!form) return;
      resetTaskForm();
      const task = JSON.parse(button.dataset.editTask);
      form.action = `/tasks/${task.id}/edit`;
      if (title) title.textContent = "Edit task";
      document.getElementById("task-title").value = task.title || "";
      document.getElementById("task-description").value = task.description || "";
      document.getElementById("task-category").value = task.category || "General";
      document.getElementById("task-priority").value = task.priority || "Medium";
      document.getElementById("task-due").value = task.due_date || "";
      document.getElementById("task-status").value = task.status || "Pending";
      openModal();
    });
  });

  const chartDataElement = document.getElementById("chart-data");
  if (chartDataElement && window.Chart) {
    const data = JSON.parse(chartDataElement.textContent);
    const statusCanvas = document.getElementById("statusChart");
    if (statusCanvas) {
      new Chart(statusCanvas, {
        type: "doughnut",
        data: {
          labels: data.statusLabels,
          datasets: [{
            data: data.statusValues,
            backgroundColor: ["#f4b66a", "#8c7cf0", "#55c6a4"],
            borderWidth: 0,
            hoverOffset: 5,
            borderRadius: 5,
            spacing: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "72%",
          plugins: {
            legend: { display: false },
            tooltip: { backgroundColor: "#20213a", padding: 12, displayColors: true }
          }
        }
      });
    }
    const categoryCanvas = document.getElementById("categoryChart");
    if (categoryCanvas) {
      new Chart(categoryCanvas, {
        type: "bar",
        data: {
          labels: data.categoryLabels,
          datasets: [{
            label: "Tasks",
            data: data.categoryValues,
            backgroundColor: ["#8c7cf0", "#55c6a4", "#f4b66a", "#ef8c9a", "#73a7ee", "#d2a0eb"],
            borderRadius: 6,
            maxBarThickness: 26
          }]
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { beginAtZero: true, ticks: { precision: 0, color: "#8a8da5" }, grid: { color: "#f0f0f6" }, border: { display: false } },
            y: { ticks: { color: "#696c83" }, grid: { display: false }, border: { display: false } }
          }
        }
      });
    }
  }
});
