(function () {
  const board = document.querySelector("[data-board-detail]");
  if (!board) {
    return;
  }

  const reorderUrl = board.dataset.boardReorderUrl;
  const statusNode = board.querySelector("[data-board-reorder-status]");

  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (const cookieChunk of cookies) {
      const cookie = cookieChunk.trim();
      if (cookie.startsWith(`${name}=`)) {
        return decodeURIComponent(cookie.slice(name.length + 1));
      }
    }
    return "";
  }

  function setStatus(message, state) {
    if (!statusNode) {
      return;
    }
    if (!message) {
      statusNode.textContent = "";
      statusNode.dataset.visible = "false";
      delete statusNode.dataset.state;
      return;
    }
    statusNode.textContent = message;
    statusNode.dataset.visible = "true";
    statusNode.dataset.state = state || "info";
  }

  function setTaskBusy(taskCard, isBusy) {
    taskCard.dataset.reorderBusy = isBusy ? "true" : "false";
    const controls = taskCard.querySelectorAll("[data-reorder-action], [data-reorder-target-list]");
    controls.forEach((control) => {
      if (isBusy) {
        control.dataset.previousDisabled = control.disabled ? "true" : "false";
        control.disabled = true;
        return;
      }
      const wasDisabled = control.dataset.previousDisabled === "true";
      control.disabled = wasDisabled;
      delete control.dataset.previousDisabled;
    });
  }

  function getTaskListSection(taskCard) {
    return taskCard.closest("[data-task-list]");
  }

  function getTaskCardsForList(taskListId) {
    const taskList = board.querySelector(`[data-task-list-id="${taskListId}"]`);
    if (!taskList) {
      return [];
    }
    return Array.from(taskList.querySelectorAll("[data-task-card]"));
  }

  function buildPayload(taskCard, action) {
    const taskId = Number(taskCard.dataset.taskId);
    const taskListSection = getTaskListSection(taskCard);
    const currentTaskListId = Number(taskListSection.dataset.taskListId);
    const currentTaskCards = getTaskCardsForList(currentTaskListId);
    const currentIndex = currentTaskCards.findIndex((card) => card === taskCard);

    if (action === "up") {
      if (currentIndex <= 0) {
        return null;
      }
      return {
        task_id: taskId,
        target_task_list_id: currentTaskListId,
        target_position: currentIndex,
      };
    }

    if (action === "down") {
      if (currentIndex < 0 || currentIndex >= currentTaskCards.length - 1) {
        return null;
      }
      return {
        task_id: taskId,
        target_task_list_id: currentTaskListId,
        target_position: currentIndex + 2,
      };
    }

    const targetSelect = taskCard.querySelector("[data-reorder-target-list]");
    if (!targetSelect || !targetSelect.value) {
      setStatus("Selecciona primero la lista destino para mover la tarea.", "error");
      return null;
    }

    const targetTaskListId = Number(targetSelect.value);
    if (!Number.isInteger(targetTaskListId) || targetTaskListId < 1) {
      setStatus("La lista destino seleccionada no es válida.", "error");
      return null;
    }

    const targetTaskCards = getTaskCardsForList(targetTaskListId);
    return {
      task_id: taskId,
      target_task_list_id: targetTaskListId,
      target_position: action === "move-start" ? 1 : targetTaskCards.length + 1,
    };
  }

  async function submitReorder(taskCard, payload) {
    setTaskBusy(taskCard, true);
    setStatus("Reordenando tarea en el tablero...", "info");

    try {
      const response = await fetch(reorderUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify(payload),
      });

      let responseData = null;
      try {
        responseData = await response.json();
      } catch (error) {
        responseData = null;
      }

      if (!response.ok || !responseData || responseData.ok !== true) {
        throw new Error("reorder_failed");
      }

      setStatus("Reordenación aplicada. Actualizando el tablero...", "success");
      window.location.reload();
    } catch (error) {
      setTaskBusy(taskCard, false);
      setStatus("No se pudo reordenar la tarea. Recarga el tablero y vuelve a intentarlo.", "error");
    }
  }

  board.addEventListener("click", (event) => {
    const button = event.target.closest("[data-reorder-action]");
    if (!button || !board.contains(button) || button.disabled) {
      return;
    }

    const taskCard = button.closest("[data-task-card]");
    if (!taskCard || taskCard.dataset.reorderBusy === "true") {
      return;
    }

    event.preventDefault();
    const payload = buildPayload(taskCard, button.dataset.reorderAction);
    if (!payload) {
      return;
    }
    submitReorder(taskCard, payload);
  });
})();
