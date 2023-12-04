(function ($) {
  "use strict";

  var fullHeight = function () {
    $(".js-fullheight").css("height", $(window).height());
    $(window).resize(function () {
      $(".js-fullheight").css("height", $(window).height());
    });
  };
  fullHeight();

  $("#sidebarCollapse").on("click", function () {
    $("#sidebar").toggleClass("active");
  });
})(jQuery);

// Fungsi Add Task
document.addEventListener("DOMContentLoaded", function () {
  const modalAdd = new bootstrap.Modal(document.getElementById("modalAdd"));
  const btnAdd = document.getElementById("btn-add");
  const btnAddTask = document.querySelector("#modalAdd button.btn-primary");
  const titleInput = document.getElementById("recipient-name");
  const descriptionInput = document.getElementById("message-text");
  const todoColumn = document.getElementById("todo");

  btnAdd.addEventListener("click", function () {
    modalAdd.show();
  });

  btnAddTask.addEventListener("click", function () {
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();

    if (title !== "" && description !== "") {
      // Buat elemen artikel baru untuk tugas
      const newTask = document.createElement("article");
      newTask.classList.add("border", "p-3", "drag");
      newTask.innerHTML = `
        <h4>${title}</h4>
        <p>${description}</p>
        <button class="badge bg-danger" onclick="deleteTask(this)">Delete</button>
        <button class="badge bg-info" onclick="editTask(this)">Edit</button>
      `;

      // Tambahkan tugas baru ke kolom "Todo"
      todoColumn.appendChild(newTask);

      // Kosongkan input setelah menambahkan tugas
      titleInput.value = "";
      descriptionInput.value = "";

      // Tutup modal setelah menambahkan tugas
      modalAdd.hide();
    }
  });
});

function deleteTask(button) {
  // Hapus elemen artikel (tugas) saat tombol "Delete" diklik
  const task = button.parentElement;
  task.remove();
}
