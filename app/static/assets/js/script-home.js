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

let todoColumn = document.getElementById("todo");

// Load data menggunakan XMLHTTPRequest
window.onload = function () {
  let xhr = new XMLHttpRequest();
  let url = "../data/data-task.json";

  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      let responses = JSON.parse(this.response);
      responses.forEach((response) => {
        // Membuat elemen-elemen HTML yang akan menampilkan tugas
        let article = document.createElement("article");
        let badgeDelete = document.createElement("button");
        let badgeEdit = document.createElement("button");
        let p = document.createElement("p");
        let h4 = document.createElement("h4");

        // Menetapkan teks judul dan deskripsi dari respons JSON ke elemen-elemen HTML
        h4.innerHTML = response.title;
        p.innerHTML = response.desc;

        // Mengatur atribut dan properti elemen <article>
        article.setAttribute("class", "border p-2 m-3 drag");
        article.setAttribute("ondragstart", "drag(event)");
        article.setAttribute("draggable", "true");
        article.setAttribute("id", response.id);

        // Mengatur atribut dan properti elemen tombol hapus
        badgeDelete.setAttribute(
          "class",
          "badge bg-danger link-underline link-underline-opacity-0 mr-3"
        );
        badgeDelete.setAttribute("id", "delete-" + response.id);
        badgeDelete.setAttribute("onclick", "deleteTask(this.id)");

        // Menambahkan
        badgeDelete.setAttribute("data-bs-toggle", "modal");
        badgeDelete.setAttribute("data-bs-target", "#modalDelete");

        // Mengatur atribut dan properti elemen tombol edit
        badgeEdit.setAttribute(
          "class",
          "badge bg-info link-underline link-underline-opacity-0 mr-3"
        );
        badgeEdit.setAttribute("id", "edit-" + response.id);
        badgeEdit.setAttribute("onclick", "editTask(this)");

        // Menambahkan
        badgeEdit.setAttribute("data-bs-toggle", "modal");
        badgeEdit.setAttribute("data-bs-target", "#modalEdit");

        // Menambahkan elemen-elemen ke dalam elemen <article>
        article.appendChild(h4);
        article.appendChild(p);
        article.appendChild(badgeDelete);
        article.appendChild(badgeEdit);

        // Menambahkan teks ke dalam tombol hapus dan edit
        badgeDelete.appendChild(document.createTextNode("Delete"));
        badgeEdit.appendChild(document.createTextNode("Edit"));

        // Menyisipkan elemen <article> ke dalam elemen yang menampung tugas (todoColumn)
        todoColumn.appendChild(article);
      });
    }
  };
  xhr.open("GET", url, true);
  xhr.send();
};

// Fungsi Add Task
document.addEventListener("DOMContentLoaded", function () {
  const modalAdd = new bootstrap.Modal(document.getElementById("modalAdd"));
  const btnAdd = document.getElementById("btn-add");
  const btnAddTask = document.querySelector("#modalAdd button.btn-primary");
  const titleInput = document.getElementById("task-title");
  const descriptionInput = document.getElementById("task-description");

  btnAdd.addEventListener("click", function () {
    modalAdd.show();
  });

  btnAddTask.addEventListener("click", function () {
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();

    if (title !== "" && description !== "") {
      // Buat elemen artikel baru untuk tugas
      const newTask = document.createElement("article");
      newTask.classList.add("border", "p-2", "m-3", "drag");
      newTask.innerHTML = `
        <h4>${title}</h4>
        <p>${description}</p>
        <button class="badge bg-danger link-underline link-underline-opacity-0 mr-3" data-bs-toggle="modal"
        data-bs-target="#modalDelete" onclick="deleteTask(this)">Delete</button>
        <button class="badge bg-info link-underline link-underline-opacity-0 mr-3" data-bs-toggle="modal"
        data-bs-target="#modalEdit" onclick="editTask(this)">Edit</button>
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
